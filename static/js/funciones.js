// Función para mostrar mensajes de notificación
    function showAppMessage(message, type = 'info') {
        const messageBox = document.getElementById('appMessageBox');
        const messageText = document.getElementById('appMessageText');

        messageText.textContent = message;
        messageBox.className = 'app-message-box show ' + type; // Añade la clase de tipo

        setTimeout(() => {
            messageBox.classList.remove('show');
        }, 5000); // Ocultar después de 5 segundos
    }

    // Inicialización de DataTables para tablas con la clase 'datatable'
    // Asegura que las tablas con esta clase se conviertan en DataTables
    function initializeDataTables() {
        if ($.fn.DataTable.isDataTable('.datatable')) {
            $('.datatable').DataTable().destroy();
        }
        $('.datatable').DataTable({
            language: {
                url: "//cdn.datatables.net/plug-ins/1.13.4/i18n/es-ES.json"
            },
            // Desactiva la inicialización automática de DataTables para evitar conflictos
            // Es mejor inicializarlas manualmente si se cargan dinámicamente.
            // bDestroy: true para permitir reinicialización.
            "retrieve": true, // Permite recuperar la instancia si ya existe
            "paging": true,   // Habilita la paginación
            "searching": true // Habilita la búsqueda
        });
    }

    // Función para cargar contenido dinámicamente según el hash de la URL
    function loadPage(pageId) {
        const contentArea = document.getElementById('dynamic-content-area');
        const allSections = document.querySelectorAll('#dynamic-content-area > section, .error-page');
        const sidebarNavLinks = document.querySelectorAll('.sidebar-nav .nav-link');

        // Ocultar todas las secciones primero
        allSections.forEach(section => {
            section.classList.add('d-none');
        });

        // Remover la clase 'active' de todos los enlaces del sidebar
        sidebarNavLinks.forEach(link => {
            link.classList.remove('active');
        });

        // Mostrar la sección solicitada
        const targetSection = document.getElementById(pageId);
        if (targetSection) {
            targetSection.classList.remove('d-none');

            // Activar el enlace del sidebar correspondiente
            const activeLink = document.querySelector(`.sidebar-nav .nav-link[href="#${pageId}"]`);
            if (activeLink) {
                activeLink.classList.add('active');
            }

            // Si la sección es un módulo que usa DataTables, inicializarla
            if (targetSection.querySelector('.datatable')) {
                initializeDataTables();
            }

            // Lógica específica para Mapa de Clientes si usa Leaflet
            if (pageId === 'mapa_clientes' && typeof L !== 'undefined') {
                // Aquí iría la lógica de inicialización del mapa Leaflet
                // Asegúrate de que el div 'mapa-clientes-container' esté visible antes de inicializar el mapa
                const mapContainer = document.getElementById('mapa-clientes-container');
                if (mapContainer && !mapContainer.hasAttribute('data-map-initialized')) {
                    // Remover el placeholder de imagen
                    const placeholderImg = mapContainer.querySelector('img');
                    if (placeholderImg) {
                        placeholderImg.remove();
                    }
                    var map = L.map('mapa-clientes-container').setView([4.7110, -74.0721], 12); // Coordenadas de ejemplo (Bogotá)
                    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
                    }).addTo(map);

                    // Ejemplo de marcador de cliente
                    // var cliente1 = L.marker([4.65, -74.05]).addTo(map)
                    //     .bindPopup('<b>Cliente: María López</b><br>Dirección: Calle 10 # 5-20')
                    //     .openPopup();
                    mapContainer.setAttribute('data-map-initialized', 'true'); // Marcar como inicializado
                } else if (mapContainer && mapContainer.hasAttribute('data-map-initialized')) {
                    // Si el mapa ya fue inicializado, solo invalida su tamaño para que se redibuje correctamente
                    if (mapContainer._leaflet_map) { // Accede a la instancia del mapa si existe
                        mapContainer._leaflet_map.invalidateSize();
                    }
                }
            }
            // Lógica para Select2 (si aplica en alguna sección)
            if (targetSection.querySelector('.select2-enabled') && $.fn.select2) {
                $(targetSection).find('.select2-enabled').select2();
            }

        } else {
            // Si la sección/página solicitada no se encuentra, mostrar 404
            document.getElementById('404').classList.remove('d-none');
        }

        // Desplazarse al inicio de la sección (con un pequeño offset para el navbar)
        window.scrollTo({ top: 0, behavior: 'smooth' }); // Siempre al inicio de la página para la vista del módulo

        // Actualizar la URL del navegador (simulación de router)
        history.pushState(null, '', `#${pageId}`);

        // Para el offcanvas en móviles, asegúrate de cerrarlo si estaba abierto
        const sidebarElement = document.getElementById('sidebar');
        const bsOffcanvas = bootstrap.Offcanvas.getInstance(sidebarElement);
        if (bsOffcanvas && bsOffcanvas._isShown) { // Verifica si el offcanvas está visible
            bsOffcanvas.hide();
        }
    }

    // Manejar la navegación inicial y de hash
    document.addEventListener('DOMContentLoaded', function() {
        const initialHash = window.location.hash.substring(1);
        // Definir todas las "páginas" o "vistas" válidas de tu aplicación
        const validPages = [
            'dashboard', 'clientes', 'productos', 'ventas', 'cobros', 'pagos',
            'inventario', 'empleados', 'usuarios', 'zonas', 'mapa_clientes',
            'seguimiento_empleados', 'configuracion', '404'
        ];

        if (initialHash && validPages.includes(initialHash)) {
            loadPage(initialHash);
        } else {
            loadPage('dashboard'); // Cargar el dashboard por defecto si no hay hash o es inválido
        }

        // Event listener para los enlaces de navegación (sidebar)
        document.querySelectorAll('.sidebar-nav .nav-link').forEach(link => {
            link.addEventListener('click', function(e) {
                const href = this.getAttribute('href');
                if (href && href.startsWith('#')) {
                    e.preventDefault();
                    const targetId = href.substring(1);
                    loadPage(targetId);
                }
            });
        });

        // Inicializar Offcanvas para la barra lateral en móviles
        const sidebarElement = document.getElementById('sidebar');
        const navbarTogglerSidebar = document.querySelector('.navbar-toggler-sidebar');
        if (navbarTogglerSidebar) {
            new bootstrap.Offcanvas(sidebarElement, {
                backdrop: true,
                scroll: true
            });
        }

        // Ocultar mensajes de alerta después de un tiempo (simulando los de Django)
        const alerts = document.querySelectorAll('.alert-custom');
        alerts.forEach(alert => {
            setTimeout(() => {
                alert.classList.add('fade'); // Añade clase para transición
                alert.addEventListener('transitionend', () => alert.remove()); // Elimina después de la transición
            }, 5000); // Ocultar después de 5 segundos
        });
    });

    // Manejar cambios en el hash de la URL (navegación hacia adelante/atrás del navegador)
    window.addEventListener('hashchange', () => {
        const currentHash = window.location.hash.substring(1);
        const validPages = [
            'dashboard', 'clientes', 'productos', 'ventas', 'cobros', 'pagos',
            'inventario', 'empleados', 'usuarios', 'zonas', 'mapa_clientes',
            'seguimiento_empleados', 'configuracion', '404'
        ];

        if (currentHash && validPages.includes(currentHash)) {
            loadPage(currentHash);
        } else {
            loadPage('404'); // Si el hash no es válido, muestra la página 404
        }
    });