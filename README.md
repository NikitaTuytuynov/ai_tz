All the necessary libraries are in **requirements.txt**<br />
<br />
/index/  - main page<br />
<br />
**API:** <br />
**Upload image:** <br />
URL: /api/images/upload<br />
Method: POST<br />
Description: Choose an image file to upload and category<br />
<br />
Return User pretiction, AI prediction<br />
<br />
<br />
**Get List of Uploaded Images:** <br />
URL: /api/images/<br />
Method: GET<br />
Description: Returns a list of uploaded images with their categories and predictions.<br />
<br />
Return example<br />
```json
[
  {
    "filename": "example.jpg",
    "categoryByUser": "food",
    "categoryByAI": ["food", "nature", "city"]
  },
  ...
]
