# accounts/management/commands/select_winners.py
"""
Manage command to select winners for draws.

Usage examples:
  # Select winners for all draws ready for results (uses generated seed per draw)
  python manage.py select_winners

  # Select winners for a specific draw with deterministic seed
  python manage.py select_winners --draw 12 --seed my-seed-123 --count 3

  # Dry-run (do not write Winner records)
  python manage.py select_winners --dry-run

  # Force re-selection even if winners already exist
  python manage.py select_winners --force
"""

from __future__ import annotations
import hashlib
import random
from typing import List, Tuple, Optional
from datetime import date, datetime

from django.core.management.base import BaseCommand
from django.utils import timezone
from django.db import transaction

from accounts.models import Draw, Entry, Winner

def make_seed(draw: Draw, provided_seed: Optional[str] = None) -> str:
    """
    Create a reproducible seed for a draw.
    If provided_seed is given, use it; otherwise derive one from draw.id + now.
    Returns a hex string.
    """
    if provided_seed:
        return str(provided_seed)
    base = f"draw-{draw.id}-{timezone.now().isoformat()}"
    return hashlib.sha256(base.encode('utf-8')).hexdigest()

def eligible_entries_for_draw(draw: Draw) -> List[int]:
    """
    Return a list of eligible Entry PKs for the draw.
    Rules applied:
      - entry.is_active must be True
      - entry.entry_time <= draw.result_date if result_date exists
    Modify filters here to match your business rules (verification, unique users, etc.)
    """
    qs = Entry.objects.filter(draw=draw, is_active=True).order_by('entry_time')
    if draw.result_date:
        qs = qs.filter(entry_time__lte=draw.result_date)
    return list(qs.values_list('id', flat=True))

def pick_winner_ids(entry_ids: List[int], count: int, seed: str) -> List[int]:
    """
    Deterministic selection using a seeded RNG.
    Returns entry ids in the order of winner positions (1..count).
    """
    if not entry_ids:
        return []
    rng = random.Random(seed)
    # shuffle then slice to keep deterministic sample order
    ids = list(entry_ids)
    rng.shuffle(ids)
    if count >= len(ids):
        return ids
    return ids[:count]

def create_winner_rows(draw: Draw, selected_entry_ids: List[int], seed: str, method: str = 'random_seeded', admin_user=None) -> List[Winner]:
    """
    Persist Winner rows for given draw and selected entry ids.
    This function deletes existing winners for the draw if any exist (atomic).
    If you prefer to keep old winners, remove the delete line and adjust accordingly.
    """
    created: List[Winner] = []
    with transaction.atomic():
        # Remove existing winners if present (explicit policy)
        Winner.objects.filter(draw=draw).delete()

        position = 1
        now_ts = timezone.now()
        for entry_id in selected_entry_ids:
            entry = Entry.objects.select_related('user').get(pk=entry_id)
            w = Winner.objects.create(
                draw=draw,
                entry=entry,
                user=entry.user,
                position=position,
                selected_at=now_ts,
                method=method,
                seed=seed,
                audit_note=f"Selected by management command at {now_ts.isoformat()}"
            )
            created.append(w)
            position += 1
    return created

class Command(BaseCommand):
    help = "Select winners for draws. Use --dry-run to preview without writing DB."

    def add_arguments(self, parser):
        parser.add_argument('--draw', type=int, help='Run selection for a specific draw id')
        parser.add_argument('--count', type=int, help='Number of winners to pick (overrides draw.winners_count)')
        parser.add_argument('--seed', type=str, help='Provide a seed to make selection reproducible')
        parser.add_argument('--force', action='store_true', help='Force selection even if winners already exist')
        parser.add_argument('--dry-run', action='store_true', help='Do not write Winner rows, just print what would happen')

    def handle(self, *args, **options):
        draw_id = options.get('draw')
        count_override = options.get('count')
        provided_seed = options.get('seed')
        force = options.get('force', False)
        dry_run = options.get('dry_run', False)

        # Select draws that are ready for result selection:
        # A draw is "ready" if result_date <= today (or end_date <= today) depending on your rules.
        today = date.today()
        if draw_id:
            draws = Draw.objects.filter(id=draw_id)
            if not draws.exists():
                self.stderr.write(self.style.ERROR(f"Draw {draw_id} not found"))
                return
        else:
            draws = Draw.objects.filter(
                # choose the rule you want: result_date <= today OR end_date <= today
            ).filter(models.Q(result_date__lte=today) | models.Q(end_date__lte=today))

        summary = []
        for draw in draws.order_by('id'):
            self.stdout.write(self.style.MIGRATE_HEADING(f"Processing draw {draw.id}: {draw.title}"))

            # Skip if winners exist and not forced
            existing_winners = list(Winner.objects.filter(draw=draw).order_by('position'))
            if existing_winners and not force:
                self.stdout.write(self.style.WARNING(f" - Skipping: {len(existing_winners)} existing winner(s). Use --force to reselect."))
                summary.append((draw.id, 'skipped_existing'))
                continue

            winners_count = count_override or getattr(draw, 'winners_count', 1)
            entry_ids = eligible_entries_for_draw(draw)
            self.stdout.write(f" - Eligible entries: {len(entry_ids)}")

            if not entry_ids:
                self.stdout.write(self.style.ERROR(" - No eligible entries, skipping"))
                summary.append((draw.id, 'no_entries'))
                continue

            seed = make_seed(draw, provided_seed)
            selected_ids = pick_winner_ids(entry_ids, winners_count, seed)
            self.stdout.write(f" - Seed: {seed}")
            self.stdout.write(f" - Selected entry ids (in position order): {selected_ids}")

            if dry_run:
                self.stdout.write(self.style.NOTICE(" - Dry run: no DB changes applied"))
                summary.append((draw.id, 'dry_run', selected_ids, seed))
                continue

            # Create Winner rows
            try:
                created = create_winner_rows(draw, selected_ids, seed, method='random_seeded')
                self.stdout.write(self.style.SUCCESS(f" - Created {len(created)} Winner rows"))
                for w in created:
                    self.stdout.write(f"    pos {w.position}: entry={w.entry_id} user={w.user.username}")
                summary.append((draw.id, 'created', [w.id for w in created], seed))
            except Exception as exc:
                self.stderr.write(self.style.ERROR(f" - Error creating winners: {exc}"))
                summary.append((draw.id, 'error', str(exc)))

        # final summary
        self.stdout.write(self.style.MIGRATE_HEADING("Summary"))
        for item in summary:
            self.stdout.write(str(item))

        self.stdout.write(self.style.SUCCESS("Selection run complete"))
