import useFileStore from '../stores/fileStore';

function FileUpload() {
  const { file, setFile, clearFile, error, setError, isLoading, setIsLoading } = useFileStore();

  const validateFile = (file) => {
    const allowedTypes = ['video/mp4', 'video/quicktime'];
    if (!allowedTypes.includes(file.type)) {
      return 'Invalid file type. Please upload an MP4 or MOV file.';
    }

    const maxSize = 800 * 1024 * 1024; // 800MB
    if (file.size > maxSize) {
      return 'File is too large. Maximum size is 800MB.';
    }

    return null; // No error
  };

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile) {
      const validationError = validateFile(selectedFile);
      if (validationError) {
        setError(validationError);
        clearFile();
      } else {
        setError('');
        setFile(selectedFile);
      }
    }
  };

  const handleAnalyze = async () => {
    if (!file) {
      setError('Please upload a file before analyzing.');
      return;
    }
    setIsLoading(true);
    setError('');
    
    try {
      // Simulate video processing with a delay
      await new Promise(resolve => setTimeout(resolve, 3000));
      console.log('Analyzing video:', file.name);
      // TODO: Implement your actual analysis logic here
    } catch (err) {
      console.log(err);
      setError('An error occurred during analysis. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="card bg-base-100 shadow-xl">
      <div className="card-body">
        <h2 className="card-title text-2xl mb-4 justify-center underline">Try it out now</h2>
        <p className="mb-4">Experience the power of EndoInsight AI firsthand. Upload your cholecystectomy video for instant analysis.</p>
        <div className="form-control">
          <label className="label">
            <span className="label-text">Upload your video (MP4 or MOV, max 800MB)</span>
          </label>
          <input
            type="file"
            className="file-input file-input-bordered w-full"
            accept=".mp4,.mov"
            onChange={handleFileChange}
            disabled={isLoading}
          />
        </div>
        {error && <div className="text-error mt-2">{error}</div>}
        {file && <div className="text-success mt-2">File uploaded: {file.name}</div>}
        <div className="card-actions justify-end mt-4">
          <button 
            className="btn btn-neutral" 
            onClick={handleAnalyze} 
            disabled={!file || isLoading}
          >
            {isLoading ? (
              <>
                <span className="loading loading-spinner"></span>
                Processing...
              </>
            ) : (
              'Analyze Video'
            )}
          </button>
        </div>
      </div>
    </div>
  );
}

export default FileUpload;