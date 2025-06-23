import pandas as pd
from loguru import logger

from nviro_fetch.common.env import env_endpoints
from nviro_fetch.fetch import fetch_nviro


def fetch_forecast(jwt_token, area_id, is_print=False):
    """Fetch weather forecast data."""
    forecast_endpoint = env_endpoints("forecasts")
    if not forecast_endpoint:
        logger.error("Forecast endpoint is not set in environment variables.")
        return {"error": "Forecast endpoint is not set in environment variables."}
    if not area_id:
        logger.error("Area ID is required to fetch forecast data.")
        return {"error": "Area ID is required to fetch forecast data."}
    # Construct the full endpoint URL with area_id
    endpoint = f"{forecast_endpoint}?area_id={area_id}"

    try:
        forecast_api = fetch_nviro(jwt_token, endpoint, is_print=is_print)
        logger.info("Forecast API response: {}", forecast_api)
        return forecast_api
    except Exception as e:
        logger.error("Error fetching forecast data: {}", e)
        return {"error": str(e)}


def forecast_to_dataframe(api_data, forecast_type="hourly"):
    """Convert forecast data to a pandas DataFrame."""
    if forecast_type not in ["hourly", "daily"]:
        logger.error("Invalid forecast type provided. Must be 'hourly' or 'daily'.")
        return pd.DataFrame()
    type = f"{forecast_type.lower()}_forecast"
    forecast_data = api_data[type]
    if not forecast_data or "error" in forecast_data:
        logger.error("Invalid forecast data provided.")
        return pd.DataFrame()

    try:
        df = pd.DataFrame(forecast_data)
        logger.info("Forecast data converted to DataFrame successfully.")
        return df
    except Exception as e:
        logger.error("Error converting forecast data to DataFrame: {}", e)
        return pd.DataFrame()
