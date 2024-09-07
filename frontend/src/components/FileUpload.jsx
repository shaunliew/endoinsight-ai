import useFileStore from '../stores/fileStore';
import medicalSvg from '../assets/medical.svg';
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

  const handleAnalyze = async () => {
    if (!file) {
      setError('Please upload a file before analyzing.');
      return;
    }
    setIsLoading(true);
    setError('');
    setAnalysisResult(null);
    
    try {
      // Simulate video processing with a delay
      await new Promise(resolve => setTimeout(resolve, 3000));
      
      // Simulate receiving analysis result with full mock data
      const mockResult = {
        analysis_result: JSON.stringify({
          "procedure_overview": "The video depicts a laparoscopic cholecystectomy procedure, showing the key steps involved in the surgical removal of the gallbladder.",
          "observations": [
            "The initial frames show the insertion of laparoscopic instruments, including graspers and dissecting tools, into the abdominal cavity.",
            "The surgeon then identifies and isolates the gallbladder, performing careful dissection around the calot's triangle region.",
            "The cystic duct and cystic artery are clearly identified, clipped, and divided to allow for the safe removal of the gallbladder.",
            "Throughout the procedure, the surgeon utilizes various techniques, such as blunt and sharp dissection, electrocautery, and grasping, to carefully separate the gallbladder from the liver bed.",
            "In the final frames, the detached gallbladder is removed through one of the port sites."
          ],
          "identification": {
            "structures": [
              "Gallbladder",
              "Cystic duct",
              "Cystic artery",
              "Liver parenchyma"
            ],
            "instruments": [
              "Laparoscopic grasper",
              "Dissecting hook or electrocautery instrument",
              "Clip applier",
              "Scissors or cutting instrument"
            ],
            "uncertainties": [
              "The exact location and relationship of the common bile duct is not clearly visible in the provided frames."
            ]
          },
          "procedural_steps": [
            "1. Placement of laparoscopic trocars and initial exploration of the abdominal cavity.",
            "2. Identification and grasping of the gallbladder fundus.",
            "3. Careful dissection of the calot's triangle to expose the cystic duct and artery.",
            "4. Clipping and division of the cystic duct and artery.",
            "5. Continued dissection to separate the gallbladder from the liver bed.",
            "6. Removal of the detached gallbladder through a port site."
          ],
          "surgical_technique": [
            "The surgeon employs a 'critical view of safety' approach, ensuring clear identification of the cystic duct and artery before division.",
            "Meticulous blunt and sharp dissection is used to carefully separate the gallbladder from the surrounding tissues, avoiding injury to adjacent structures.",
            "Electrocautery is utilized for hemostasis during the dissection and gallbladder removal process."
          ],
          "critical_moments": [
            "Identification and isolation of the cystic duct and artery before clipping and division, to prevent bile duct injuries.",
            "Ensuring the 'critical view of safety' is achieved before dividing any structures, to maintain a clear understanding of the anatomy.",
            "Careful dissection of the gallbladder from the liver bed to avoid perforation or bleeding."
          ],
          "clinical_significance": [
            "The 'critical view of safety' technique is a crucial step in laparoscopic cholecystectomy to minimize the risk of bile duct injuries, a serious complication.",
            "Proper identification and isolation of the cystic duct and artery are essential to prevent inadvertent division of the common bile duct.",
            "Meticulous hemostasis and careful tissue handling during gallbladder removal help to reduce post-operative complications, such as bleeding or bile leaks."
          ],
          "educational_summary": [
            "This video demonstrates the standard steps of a laparoscopic cholecystectomy procedure, highlighting the importance of careful dissection and precise identification of anatomical structures.",
            "The use of the 'critical view of safety' technique is clearly illustrated, emphasizing its crucial role in preventing major complications, such as bile duct injuries.",
            "The video showcases effective instrument handling and tissue manipulation skills, which are essential for performing this minimally invasive surgical procedure safely and efficiently."
          ]
        }),
        output_video_url: "https://storage.googleapis.com/endoinsight-output/output/c30976d9-bc3e-438d-9ac9-de55010bae77_output.mp4"
      };
      
      setAnalysisResult(mockResult);
    } catch (err) {
      console.error(err);
      setError('An error occurred during analysis. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
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
  );
}

export default FileUpload;