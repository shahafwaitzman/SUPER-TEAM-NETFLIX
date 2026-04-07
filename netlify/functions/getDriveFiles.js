exports.handler = async (event) => {
  try {
    const { folderId } = JSON.parse(event.body || '{}');
    console.log('[getDriveFiles] Called with folderId:', folderId);

    if (!folderId) {
      console.log('[getDriveFiles] Error: folderId is required');
      return {
        statusCode: 400,
        body: JSON.stringify({ error: 'folderId required' })
      };
    }

    // Google Drive API call
    // SECURITY: API key should be provided via environment variable, not hardcoded
    const apiKey = process.env.GOOGLE_DRIVE_API_KEY;
    if (!apiKey) {
      console.log('[getDriveFiles] Error: GOOGLE_DRIVE_API_KEY environment variable not set');
      return {
        statusCode: 500,
        body: JSON.stringify({ error: 'API configuration missing' })
      };
    }
    const url = `https://www.googleapis.com/drive/v3/files?q='${folderId}' in parents&fields=id,name,mimeType,webContentLink&key=${apiKey}`;
    console.log('[getDriveFiles] Calling Drive API for folder:', folderId);

    const response = await fetch(url);
    const data = await response.json();
    console.log('[getDriveFiles] API response status:', response.status, 'Files found:', data.files?.length || 0);

    if (!response.ok) {
      console.error('[getDriveFiles] API error:', data.error?.message);
      return {
        statusCode: response.status,
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ error: data.error?.message || 'Drive API failed' })
      };
    }

    return {
      statusCode: 200,
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(data)
    };
  } catch (error) {
    console.error('[getDriveFiles] Exception:', error.message);
    return {
      statusCode: 500,
      body: JSON.stringify({ error: error.message })
    };
  }
};
