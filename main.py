import resource
import uuid
import cv2

from flask import Flask, render_template, request
from project import mosavid

# from PIL import Image

app = Flask(
    __name__,
    template_folder="project/templates",
    static_folder="project/static",
)

TEMP_CONTENT_PATH = "/tmp"


@app.route("/")
def root() -> str:
    return render_template("index.html")


@app.route("/create_mosaic", methods=["POST"])
def create_mosaic() -> str:
    soft_memory_limit_in_bytes = 200000000
    soft, hard = resource.getrlimit(resource.RLIMIT_AS)
    resource.setrlimit(resource.RLIMIT_AS, (soft_memory_limit_in_bytes, hard))

    image = request.files["image"]
    video = request.files["video"]
    

    image_path = f"{TEMP_CONTENT_PATH}/{uuid.uuid1()}"
    video_path = f"{TEMP_CONTENT_PATH}/{uuid.uuid1()}"
    image.save(image_path)
    video.save(video_path)

    mosaic = mosavid.create_mosaic_from_video(
        target_img_path=image_path, source_video_path=video_path
    )
    mosaic_file_name = f"{uuid.uuid1()}.png"
    mosaic_file_path = f"{TEMP_CONTENT_PATH}/{mosaic_file_name}"
    cv2.imwrite(filename=mosaic_file_path, img=mosaic)

    return render_template("index.html", mosaic=mosaic_file_name)


if __name__ == "__main__":
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    # Flask's development server will automatically serve static files in
    # the "static" directory. See:
    # http://flask.pocoo.org/docs/1.0/quickstart/#static-files. Once deployed,
    # App Engine itself will serve those files as configured in app.yaml.
    TEMP_CONTENT_PATH = "project/static"

    soft_memory_limit_in_bytes = 200000000
    soft, hard = resource.getrlimit(resource.RLIMIT_AS)
    resource.setrlimit(resource.RLIMIT_AS, (soft_memory_limit_in_bytes, hard))

    app.run(host="127.0.0.1", port=5000, debug=True)
