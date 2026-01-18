<style>
/* ===== GLOBAL STYLES ===== */
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    min-height: 100vh;
    color: #333;
    line-height: 1.6;
}

/* ===== SIDEBAR STYLES ===== */
#sidebar {
    position: fixed;
    top: 0;
    left: 0;
    height: 100vh;
    width: 280px;
    background: linear-gradient(180deg, #2c3e50 0%, #34495e 100%);
    box-shadow: 4px 0 15px rgba(0, 0, 0, 0.1);
    z-index: 1000;
    transition: all 0.3s ease;
    border-right: 3px solid #3498db;
}

.sidebar-header {
    padding: 30px 20px;
    background: rgba(0, 0, 0, 0.2);
    text-align: center;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.sidebar-header h3 {
    color: #fff;
    font-size: 1.5rem;
    font-weight: 600;
    margin-bottom: 8px;
    text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
}

.sidebar-header small {
    color: #bdc3c7;
    font-size: 0.85rem;
    font-weight: 300;
}

.list-unstyled {
    padding: 20px 0;
}

.list-unstyled li {
    margin: 5px 0;
    position: relative;
    transition: all 0.3s ease;
}

.list-unstyled li.active {
    background: rgba(52, 152, 219, 0.2);
    border-left: 4px solid #3498db;
}

.list-unstyled li:hover {
    background: rgba(52, 152, 219, 0.1);
    border-left: 4px solid #2980b9;
}

.list-unstyled li a {
    display: flex;
    align-items: center;
    padding: 15px 25px;
    color: #ecf0f1;
    text-decoration: none;
    font-weight: 500;
    transition: all 0.3s ease;
    font-size: 0.95rem;
}

.list-unstyled li a:hover {
    color: #3498db;
    transform: translateX(5px);
}

.list-unstyled li a i {
    margin-right: 12px;
    font-size: 1.1rem;
    width: 20px;
    text-align: center;
}

/* ===== CONTENT AREA STYLES ===== */
#content {
    margin-left: 280px;
    padding: 30px;
    min-height: 100vh;
    transition: all 0.3s ease;
}

.dashboard-section {
    display: none;
    animation: fadeIn 0.5s ease-in;
}

.dashboard-section.active {
    display: block;
}

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}

/* ===== CARD STYLES ===== */
.card {
    background: rgba(255, 255, 255, 0.95);
    border: none;
    border-radius: 15px;
    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
    transition: all 0.3s ease;
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.2);
    overflow: hidden;
}

.card:hover {
    transform: translateY(-5px);
    box-shadow: 0 15px 35px rgba(0, 0, 0, 0.15);
}

.card-header {
    background: linear-gradient(135deg, #3498db, #2980b9);
    color: white;
    border: none;
    padding: 20px 25px;
    font-weight: 600;
    font-size: 1.1rem;
}

.card-body {
    padding: 25px;
}

/* ===== STATS CARDS ===== */
.col-md-4 .card {
    background: linear-gradient(135deg, #fff 0%, #f8f9fa 100%);
    border-left: 4px solid #3498db;
}

.col-md-4 .card:hover {
    background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
}

.col-md-4 .card-body h6 {
    color: #7f8c8d;
    font-size: 0.9rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.col-md-4 .card-body h3 {
    color: #2c3e50;
    font-size: 2.2rem;
    font-weight: 700;
    margin: 10px 0 0 0;
}

/* ===== BUTTON STYLES ===== */
.btn {
    padding: 10px 20px;
    border-radius: 8px;
    font-weight: 600;
    text-decoration: none;
    transition: all 0.3s ease;
    border: none;
    cursor: pointer;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    font-size: 0.9rem;
}

.btn-sm {
    padding: 8px 16px;
    font-size: 0.85rem;
}

.btn-primary {
    background: linear-gradient(135deg, #3498db, #2980b9);
    color: white;
    box-shadow: 0 4px 15px rgba(52, 152, 219, 0.3);
}

.btn-primary:hover {
    background: linear-gradient(135deg, #2980b9, #3498db);
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(52, 152, 219, 0.4);
}

.btn-warning {
    background: linear-gradient(135deg, #f39c12, #e67e22);
    color: white;
    box-shadow: 0 4px 15px rgba(243, 156, 18, 0.3);
}

.btn-warning:hover {
    background: linear-gradient(135deg, #e67e22, #f39c12);
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(243, 156, 18, 0.4);
}

.btn-outline-primary {
    background: transparent;
    border: 2px solid #3498db;
    color: #3498db;
}

.btn-outline-primary:hover {
    background: #3498db;
    color: white;
    transform: translateY(-2px);
}

.btn-outline-secondary {
    background: transparent;
    border: 2px solid #95a5a6;
    color: #95a5a6;
}

.btn-outline-secondary:hover {
    background: #95a5a6;
    color: white;
    transform: translateY(-2px);
}

.btn-outline-warning {
    background: transparent;
    border: 2px solid #f39c12;
    color: #f39c12;
}

.btn-outline-warning:hover {
    background: #f39c12;
    color: white;
    transform: translateY(-2px);
}

/* ===== FORM STYLES ===== */
.form-control {
    border: 2px solid #ecf0f1;
    border-radius: 8px;
    padding: 12px 15px;
    font-size: 0.95rem;
    transition: all 0.3s ease;
    background: rgba(255, 255, 255, 0.9);
}

.form-control:focus {
    border-color: #3498db;
    box-shadow: 0 0 0 3px rgba(52, 152, 219, 0.1);
    background: white;
}

.form-label {
    font-weight: 600;
    color: #2c3e50;
    margin-bottom: 8px;
}

.form-check-input:checked {
    background-color: #3498db;
    border-color: #3498db;
}

/* ===== ALERT STYLES ===== */
.alert {
    border: none;
    border-radius: 10px;
    padding: 15px 20px;
    font-weight: 500;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
}

.alert-success {
    background: linear-gradient(135deg, #d4edda, #c3e6cb);
    color: #155724;
    border-left: 4px solid #28a745;
}

.alert-info {
    background: linear-gradient(135deg, #d1ecf1, #bee5eb);
    color: #0c5460;
    border-left: 4px solid #17a2b8;
}

.alert-warning {
    background: linear-gradient(135deg, #fff3cd, #ffeaa7);
    color: #856404;
    border-left: 4px solid #ffc107;
}

.alert-danger {
    background: linear-gradient(135deg, #f8d7da, #f5c6cb);
    color: #721c24;
    border-left: 4px solid #dc3545;
}

/* ===== LIST GROUP STYLES ===== */
.list-group-item {
    background: rgba(255, 255, 255, 0.9);
    border: 1px solid rgba(0, 0, 0, 0.1);
    border-radius: 10px !important;
    margin-bottom: 10px;
    padding: 20px;
    transition: all 0.3s ease;
}

.list-group-item:hover {
    background: white;
    transform: translateX(5px);
    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
}

/* ===== CHART CONTAINER ===== */
.chart-container {
    position: relative;
    height: 250px;
    width: 100%;
    background: rgba(255, 255, 255, 0.8);
    border-radius: 10px;
    padding: 20px;
}

/* ===== DETAILS/SECTION STYLES ===== */
details {
    background: rgba(255, 255, 255, 0.8);
    border-radius: 10px;
    padding: 15px;
    margin-top: 15px;
}

summary {
    font-weight: 600;
    color: #3498db;
    cursor: pointer;
    transition: color 0.3s ease;
}

summary:hover {
    color: #2980b9;
}

.section-title {
    color: #2c3e50;
    font-weight: 600;
    margin-bottom: 20px;
    padding-bottom: 10px;
    border-bottom: 2px solid #3498db;
    display: flex;
    align-items: center;
}

.section-title i {
    margin-right: 10px;
    color: #3498db;
}

/* ===== RESPONSIVE DESIGN ===== */
@media (max-width: 768px) {
    #sidebar {
        width: 100%;
        height: auto;
        position: relative;
    }
    
    #content {
        margin-left: 0;
        padding: 20px;
    }
    
    .sidebar-header {
        padding: 20px;
    }
    
    .list-unstyled {
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
        padding: 10px;
    }
    
    .list-unstyled li {
        flex: 1;
        min-width: 150px;
        margin: 5px;
    }
    
    .card-body {
        padding: 15px;
    }
    
    .btn {
        width: 100%;
        margin-bottom: 10px;
    }
}

/* ===== GRID GAPS ===== */
.g-3 {
    gap: 1rem !important;
}

.row.g-3 {
    margin: 0 -0.5rem;
}

.row.g-3 > * {
    padding: 0 0.5rem;
}

/* ===== TEXT STYLES ===== */
.text-muted {
    color: #7f8c8d !important;
}

.small {
    font-size: 0.85rem;
}

.mb-0 { margin-bottom: 0 !important; }
.mb-1 { margin-bottom: 0.5rem !important; }
.mb-2 { margin-bottom: 1rem !important; }
.mb-3 { margin-bottom: 1.5rem !important; }
.mb-4 { margin-bottom: 2rem !important; }

.mt-2 { margin-top: 0.5rem !important; }
.mt-3 { margin-top: 1rem !important; }
.mt-4 { margin-top: 1.5rem !important; }

.me-1 { margin-right: 0.25rem !important; }
.me-2 { margin-right: 0.5rem !important; }

.ms-2 { margin-left: 0.5rem !important; }

/* ===== CUSTOM SCROLLBAR ===== */
::-webkit-scrollbar {
    width: 8px;
}

::-webkit-scrollbar-track {
    background: #f1f1f1;
    border-radius: 10px;
}

::-webkit-scrollbar-thumb {
    background: linear-gradient(135deg, #3498db, #2980b9);
    border-radius: 10px;
}

::-webkit-scrollbar-thumb:hover {
    background: linear-gradient(135deg, #2980b9, #3498db);
}

/* ===== ANIMATIONS ===== */
@keyframes pulse {
    0% { transform: scale(1); }
    50% { transform: scale(1.05); }
    100% { transform: scale(1); }
}

.pulse {
    animation: pulse 2s infinite;
}

/* ===== GLOW EFFECTS ===== */
.glow {
    box-shadow: 0 0 20px rgba(52, 152, 219, 0.5);
}

/* ===== GRADIENT TEXT ===== */
.gradient-text {
    background: linear-gradient(135deg, #3498db, #9b59b6);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

/* ===== LOADING STATES ===== */
.loading {
    opacity: 0.7;
    pointer-events: none;
    position: relative;
}

.loading::after {
    content: '';
    position: absolute;
    top: 50%;
    left: 50%;
    width: 20px;
    height: 20px;
    border: 2px solid #f3f3f3;
    border-top: 2px solid #3498db;
    border-radius: 50%;
    animation: spin 1s linear infinite;
}

@keyframes spin {
    0% { transform: translate(-50%, -50%) rotate(0deg); }
    100% { transform: translate(-50%, -50%) rotate(360deg); }
}

/* ===== PRINT STYLES ===== */
@media print {
    #sidebar {
        display: none;
    }
    
    #content {
        margin-left: 0;
    }
    
    .btn {
        display: none;
    }
    
    .card {
        box-shadow: none;
        border: 1px solid #ddd;
    }
}
</style>