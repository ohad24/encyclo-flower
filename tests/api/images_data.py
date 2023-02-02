upload_file_multi_params = [
    {
        "metadata": {},
        "file_name": "IMG_with_exif.jpg",
        "test_name": "Minimum metadata + with gps data",
    },
    {
        "metadata": {
            "description": "test image",
            "content_category": "פרי",
            "plant_id": "sfdm76",
            "month_taken": "דצמבר",
            "location_name": "כרמל",
        },
        "file_name": "IMG_with_exif.jpg",
        "test_name": "Maximum metadata + with gps data",
    },
    {
        "metadata": {},
        "file_name": "58NY77V207Q7H06.jpg",
        "test_name": "Minimum metadata + with no gps data",
    },
    {
        "metadata": {
            "description": "test image",
            "what_in_image": "פרי",
            "plant_id": "sfdm76",
        },
        "file_name": "58NY77V207Q7H06.jpg",
        "test_name": "Maximum metadata + with no gps data",
    },
]
