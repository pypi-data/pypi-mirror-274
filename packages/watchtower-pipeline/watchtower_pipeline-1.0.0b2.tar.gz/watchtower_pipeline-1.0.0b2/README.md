# Watchtower Pipeline

A Python package to generate data to be displayed in [Watchtower](https://watchtower.blender.org/).

Follow these instructions to deploy Watchtower in your production pipeline.

## Requirements
* Python 3.9+
* A source of production data (shots, assets, tasks, etc.)

## Setup

* Create a new folder, step into it and run:
* `python -m venv .venv`
* `source .venv/bin/activate`
* `pip install watchtower-pipeline`

### ... with example data
To create an example project that will give you an idea of how the pipeline works:

* Run `python -m watchtower_pipeline.example -b`
* Navigate to the `watchtower` folder and run `python -m http.server`

### ... with Kitsu-sourced data
If you have a working Kitsu (and Zou) installation and want to extract and visualize data from it:

* Create a `.env.local` file as follows:

  ```
  KITSU_DATA_SOURCE_URL=https://<your-kitsu-instance>/api
  KITSU_DATA_SOURCE_USER_EMAIL=user@example.org
  KITSU_DATA_SOURCE_USER_PASSWORD=password
  ```

* Run `python -m watchtower_pipeline.kitsu -b`
* Copy the content of the `watchtower` folder into your webserver
* Running the command without the `-b` flag will only fetch the data, and place it in a directory 
  called `public/data`, which can then be synced to where the `watchtower` folder has been placed.

### ... with custom-sourced data
If you use a different production/asset tracking service, some scripting will be required.  
Check `docs/integration.md` and `docs/develop-pipeline.md`.
