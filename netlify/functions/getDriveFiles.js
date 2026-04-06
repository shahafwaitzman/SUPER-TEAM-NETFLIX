exports.handler = async (event) => {
  try {
    const { folderId } = JSON.parse(event.body || '{}');

    if (!folderId) {
      return {
        statusCode: 400,
        body: JSON.stringify({ error: 'folderId required' })
      };
    }

    // Google Drive API call
    const apiKey = 'AIzaSyB1hH50REJm_hu71AjYO8e4m3BdQC6GQ0g';
    const url = `https://www.googleapis.com/drive/v3/files?q='${folderId}' in parents&fields=id,name,mimeType,webContentLink&key=${apiKey}`;

    const response = await fetch(url);
    const files = await response.json();

    return {
      statusCode: 200,
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(files)
    };
  } catch (error) {
    console.error('Error:', error);
    return {
      statusCode: 500,
      body: JSON.stringify({ error: error.message })
    };
  }
};
