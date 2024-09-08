import useFileStore from '../stores/fileStore';
import medicalSvg from '../assets/medical.svg';
import axios from 'axios';
import { useState } from 'react';
function FileUpload() {
  const { 
    file, 
    setFile, 
    clearFile, 
    error, 
    setError, 
    isLoading, 
    setIsLoading, 
    setAnalysisResult,
    resetAnalysis 
  } = useFileStore();

  const [showModal, setShowModal] = useState(false);

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
        resetAnalysis(); // Reset analysis when a new file is uploaded
      }
    }
  };
  
  const handleCloseModal = () => {
    setShowModal(false);
  };

  const handleAnalyze = async () => {
    if (!file) {
      setError('Please upload a file before analyzing.');
      return;
    }
    setIsLoading(true);
    setError('');
    setAnalysisResult(null);
    
    try {
      const formData = new FormData();
      formData.append('file', file);

      const response = await axios.post('http://localhost:8000/api/process_video/', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      if (response.data.success) {
        setAnalysisResult(response.data.content);
        setShowModal(true);
      } else {
        throw new Error(response.data.message || 'An error occurred during analysis.');
      }
    } catch (err) {
      console.error(err);
      setError(err.message || 'An error occurred during analysis. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <>
      <div className="card bg-base-100 border shadow-xl">
        <div className="card-body">
          <h2 className="card-title text-2xl mb-4 justify-center underline">Try it out now</h2>
          <p className="">Experience the power of EndoInsight AI firsthand. Upload your cholecystectomy video for instant analysis.</p>
          <div className="flex justify-center justify-items-center mb-4 w-128 h-64">
            <img src={medicalSvg} alt="Upload video" className="justify-center" />
          </div>

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

      {/* Modal */}
      {showModal && (
        <div className="modal modal-open">
          <div className="modal-box">
            <h3 className="font-bold text-lg">Video Processing Complete!</h3>
            <p className="py-4">Your video has been successfully processed. You can now view the analysis results below.</p>
            <div className="modal-action">
              <button className="btn btn-neutral" onClick={handleCloseModal}>Close</button>
            </div>
          </div>
        </div>
      )}
    </>
  );
}

export default FileUpload;