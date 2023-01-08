__all__ = [
    "ExplosionWeather"
]

class ExplosionWeather(object):

    location_name : str
    location_region : str
    location_country : str

    condition_label : str
    condition_icon : str

    wind_kph : float
    wind_direction : str
    precipitation_rain : float
    precipitation_snow : float

    humidity : float
    cloud : float
    feels_like : str

    @classmethod
    def from_response(cls, resp : dict) -> "ExplosionWeather":
        
        assoc = {
            "location_name" : resp["location"]["name"],
            "location_region" : resp["location"]["region"],
            "location_country" : resp["location"]["country"],
            "condition_label" : resp["current"]["condition"]["text"],
            "condition_icon" : resp["current"]["condition"]["icon"],
            "wind_kph" : resp["current"]["wind_kph"],
            "wind_direction" : resp["current"]["wind_dir"],
            "precipitation_rain" : resp["current"]["precip_mm"],
            "precipitation_snow" : resp["current"]["precip_in"],
            "humidity" : resp["current"]["humidity"],
            "cloud" : resp["current"]["cloud"],
            "feels_like" : resp["current"]["feelslike_c"],
        }

        ew = cls()

        for k, v in assoc:
            setattr(ew, k, v)

        return ew
