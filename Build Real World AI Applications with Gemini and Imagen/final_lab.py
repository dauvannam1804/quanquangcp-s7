import vertexai
from vertexai.preview.vision_models import ImageGenerationModel
from vertexai.generative_models import GenerativeModel, Part, Image

# ======================
# Task 1
# ======================
def generate_bouquet_image(prompt: str, project_id: str, location: str, output_file: str):
    """Generate bouquet image and save locally"""
    vertexai.init(project=project_id, location=location)

    model = ImageGenerationModel.from_pretrained("imagen-3.0-generate-002")
    images = model.generate_images(
        prompt=prompt,
        number_of_images=1,
        seed=1,
        add_watermark=False,
    )

    # Lưu ảnh
    images[0].save(location=output_file)
    print(f"Image saved at {output_file}")
    return output_file


# ======================
# Task 2
# ======================
def analyze_bouquet_image(image_path: str, project_id: str, location: str):
    """Analyze image using Gemini multimodal model with streaming"""
    vertexai.init(project=project_id, location=location)

    model = GenerativeModel("gemini-2.0-flash-001")

    # Load file ảnh và gói thành input multimodal
    image = Image.load_from_file(image_path)
    image_part = Part.from_image(image)

    # Streaming output
    responses = model.generate_content(
        [image_part, "Generate a birthday wish based on this bouquet image."],
        stream=True,
    )

    print("AI Birthday Wishes:")
    for response in responses:
        print(response.text, end="")  # In ra liên tục
    print("\nDone!")


# ======================
# Run Challenge Lab
# ======================
if __name__ == "__main__":
    PROJECT_ID = "qwiklabs-gcp-xxxxxxx"   # thay bằng Project ID trong lab
    LOCATION = "us-central1"              # hoặc region mà lab chỉ định
    OUTPUT_FILE = "bouquet.jpeg"

    # Task 1
    generate_bouquet_image(
        prompt="Create an image containing a bouquet of 2 sunflowers and 3 roses",
        project_id=PROJECT_ID,
        location=LOCATION,
        output_file=OUTPUT_FILE,
    )

    # Task 2
    analyze_bouquet_image(
        image_path=OUTPUT_FILE,
        project_id=PROJECT_ID,
        location=LOCATION,
    )

# /usr/bin/python3 /final_lab.py 
