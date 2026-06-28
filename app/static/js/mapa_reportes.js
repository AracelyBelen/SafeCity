document.addEventListener("DOMContentLoaded", function () {

    const mapaDiv = document.getElementById("map");

    if (!mapaDiv) {
        return;
    }

    const latInput = document.getElementById("latitud");
    const lngInput = document.getElementById("longitud");

    const mapContainer = document.getElementById("map-container");

    const mapa = L.map("map").setView(
        [-16.5, -68.15], // La Paz / El Alto
        12
    );

    L.tileLayer(
        "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
        {
            attribution: "&copy; OpenStreetMap"
        }
    ).addTo(mapa);

    let marcador = null;
    let seleccionManual = false;

    function mostrarMensaje(texto, tipo = "success") {

        const anterior = document.getElementById("msg-ubicacion");

        if (anterior) {
            anterior.remove();
        }

        const mensaje = document.createElement("div");

        mensaje.id = "msg-ubicacion";
        mensaje.className = `alert alert-${tipo} mt-3`;

        mensaje.innerHTML = `
            <i class="ti ti-circle-check me-2"></i>
            ${texto}
        `;

        const contenedor = document.querySelector(".loc-btns");

        if (contenedor) {
            contenedor.insertAdjacentElement(
                "afterend",
                mensaje
            );
        }

        setTimeout(() => {
            mensaje.remove();
        }, 3000);
    }

    function actualizarUbicacion(lat, lng) {

        if (marcador) {
            mapa.removeLayer(marcador);
        }

        marcador = L.marker([lat, lng]).addTo(mapa);

        mapa.setView([lat, lng], 17);

        latInput.value = lat;
        lngInput.value = lng;
    }

    mapa.on("click", function (e) {

        if (!seleccionManual) {
            return;
        }

        actualizarUbicacion(
            e.latlng.lat,
            e.latlng.lng
        );

        mostrarMensaje(
            "Ubicación seleccionada correctamente."
        );

        seleccionManual = false;
    });

    const botonUbicacion = document.getElementById("btnUbicacion");

    if (botonUbicacion) {

        botonUbicacion.addEventListener("click", function () {

            if (!navigator.geolocation) {

                mostrarMensaje(
                    "Tu navegador no permite obtener la ubicación.",
                    "danger"
                );

                return;
            }

            seleccionManual = false;

            navigator.geolocation.getCurrentPosition(

                function (pos) {

                    if (mapContainer) {

                        mapContainer.style.display = "block";

                        setTimeout(function () {
                            mapa.invalidateSize();
                        }, 200);
                    }

                    actualizarUbicacion(
                        pos.coords.latitude,
                        pos.coords.longitude
                    );

                    mostrarMensaje(
                        "Ubicación obtenida correctamente."
                    );

                },

                function (error) {

                    let mensaje = "No fue posible obtener tu ubicación.";

                    switch (error.code) {

                        case error.PERMISSION_DENIED:
                            mensaje = "Debes permitir el acceso a tu ubicación en el navegador.";
                            break;

                        case error.POSITION_UNAVAILABLE:
                            mensaje = "No se pudo determinar tu ubicación. Verifica que la ubicación o el GPS estén activados.";
                            break;

                        case error.TIMEOUT:
                            mensaje = "La solicitud de ubicación tardó demasiado.";
                            break;
                    }

                    mostrarMensaje(
                        mensaje,
                        "danger"
                    );
                },

                {
                    enableHighAccuracy: true,
                    timeout: 10000,
                    maximumAge: 0
                }
            );
        });
    }

    const botonSeleccionar = document.getElementById("btnSeleccionar");

    if (botonSeleccionar) {

        botonSeleccionar.addEventListener("click", function () {

            seleccionManual = true;

            if (mapContainer) {

                mapContainer.style.display = "block";

                setTimeout(function () {
                    mapa.invalidateSize();
                }, 200);
            }

            mostrarMensaje(
                "Haz clic en el mapa para seleccionar la ubicación."
            );
        });
    }
});