All the necessary libraries are in **requirements.txt**

/index/  - main page

**API:**
**Upload image:**
URL: /api/images/upload
Method: POST
Description: Choose an image file to upload and category

Return User pretiction, AI prediction


**Get List of Uploaded Images:**
URL: /api/images/
Method: GET
Description: Returns a list of uploaded images with their categories and predictions.

Return example
[
    {
        "filename": "example.jpg",
        "categoryByUser": "food",
        "categoryByAI": ["food", "nature", "city"]
    },
    ...
]
