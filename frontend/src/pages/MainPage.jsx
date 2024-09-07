import Hero from "../components/Hero";
import Timeline from "../components/Timeline";
import FileUpload from "../components/FileUpload";
import AnalysisResultCard from "../components/AnalysisResultCard";
import useFileStore from '../stores/fileStore';

function MainPage() {
  const { analysisResult } = useFileStore();

  return (
    <div className="container mx-auto px-4 py-8">
      <Hero />
      <div className="grid md:grid-cols-2 gap-8">
        <div className="card bg-base-100 shadow-xl border">
          <div className="card-body flex flex-col items-center">
            <h2 className="card-title text-2xl mb-4 justify-center underline">How It Works</h2>
            <Timeline />
          </div>
        </div>
        
        <FileUpload />
      </div>
      
      {analysisResult && (
        <div className="mt-8">
          <AnalysisResultCard result={analysisResult} />
        </div>
      )}
      
      <div className="mt-8">
        <div className="alert alert-info">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" className="stroke-current shrink-0 w-6 h-6"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
          <span>EndoInsight AI is for educational purposes only. Always consult with qualified medical professionals for clinical decisions.</span>
        </div>
      </div>
    </div>
  );
}

export default MainPage;