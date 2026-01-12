from django import forms
from django.utils.safestring import mark_safe
import json


class YandexMapLocationWidget(forms.Widget):
    class Media:
        js = (

            "https://api-maps.yandex.ru/2.1/?apikey=c4573bb1-b105-4461-b915-d9e7f3aee007&lang=ru_RU",
        )

    def __init__(self, lat_field='latitude', lng_field='longitude', default_center=(41.3126, 69.2401), zoom=12, *args,
                 **kwargs):
        super().__init__(*args, **kwargs)
        self.lat_field = lat_field
        self.lng_field = lng_field
        self.default_center = default_center
        self.zoom = zoom

    def render(self, name, value, attrs=None, renderer=None):
        attrs = attrs or {}
        lat_val = '' if value is None else value
        lng_val = attrs.get('initial_lng', '')  # form will set this attr in __init__

        map_id = f"yandex_map_{name}"
        lat_id = f"id_{self.lat_field}"
        lng_id = f"id_{self.lng_field}"

        lat_json = json.dumps(lat_val)
        lng_json = json.dumps(lng_val)
        default_center_json = json.dumps(self.default_center)

        html = f"""
        <div class="yandex-map-widget" style="flex-grow:1">
          <div id="{map_id}" style="width: 100%; height: 400px; margin-bottom: 8px;"></div>

          <!-- Hidden inputs: name attributes must match model field names -->
          <input type="hidden" id="{lat_id}" name="{self.lat_field}" value={lat_json}>
        </div>

        <script>
        (function() {{
            var mapId = "{map_id}";
            var latInputId = "{lat_id}";
            var lngInputId = "{lng_id}";
            var defaultCenter = {default_center_json};
            var defaultZoom = {self.zoom};

            function initMap() {{
                if (typeof ymaps === 'undefined' || !ymaps.ready) {{
                    // wait until ymaps is available
                    var poll = setInterval(function() {{
                        if (typeof ymaps !== 'undefined' && ymaps.ready) {{
                            clearInterval(poll);
                            ymaps.ready(initMap);
                        }}
                    }}, 200);
                    return;
                }}

                try {{
                    var latInput = document.getElementById(latInputId);
                    var lngInput = document.getElementById(lngInputId);
                    if (!latInput || !lngInput) return;
                    console.log(lngInput);

                    function parseVal(el) {{
                        var v = parseFloat(el.value);
                        return isNaN(v) ? null : v;
                    }}

                    var lat = parseVal(latInput);
                    var lng = parseVal(lngInput);

                    var center = defaultCenter;
                    if (lat !== null && lng !== null) {{
                        center = [lat, lng];
                    }}

                    var map = new ymaps.Map(mapId, {{
                        center: center,
                        zoom: defaultZoom,
                        controls: ['zoomControl', 'fullscreenControl']
                    }});

                    var placemark = null;
                    function addPlacemark(coords) {{
                        if (placemark) map.geoObjects.remove(placemark);
                        placemark = new ymaps.Placemark(coords, {{}}, {{
                            preset: 'islands#redDotIcon',
                            draggable: true
                        }});
                        map.geoObjects.add(placemark);
                        placemark.events.add('dragend', function () {{
                            var c = placemark.geometry.getCoordinates();
                            latInput.value = c[0].toFixed(6);
                            lngInput.value = c[1].toFixed(6);
                        }});
                    }}

                    // If values exist (edit form), place marker there
                    if (lat !== null && lng !== null) {{
                        addPlacemark([lat, lng]);
                        map.setCenter([lat, lng]);
                    }}

                    // Click on map sets marker & inputs
                    map.events.add('click', function(e) {{
                        var coords = e.get('coords');
                        addPlacemark(coords);
                        latInput.value = coords[0].toFixed(6);
                        lngInput.value = coords[1].toFixed(6);
                    }});

                }} catch (err) {{
                    console.error('YandexMap widget init error:', err);
                }}
            }}

            // start
            if (typeof ymaps !== 'undefined' && ymaps.ready) {{
                ymaps.ready(initMap);
            }} else {{
                // dynamic loader fallback
                var scriptUrl = "https://api-maps.yandex.ru/2.1/?lang=ru_RU";
                if (!document.querySelector('script[data-yandex-maps]')) {{
                    var s = document.createElement('script');
                    s.src = scriptUrl;
                    s.setAttribute('data-yandex-maps', '1');
                    s.onload = function() {{ ymaps.ready(initMap); }};
                    document.head.appendChild(s);
                }} else {{
                    var poll = setInterval(function() {{
                        if (typeof ymaps !== 'undefined' && ymaps.ready) {{
                            clearInterval(poll);
                            ymaps.ready(initMap);
                        }}
                    }}, 200);
                }}
            }}
        }})();
        </script>
        """
        return mark_safe(html)
