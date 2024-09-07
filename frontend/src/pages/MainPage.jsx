// import Hero from "../components/Hero";
import Timeline from "../components/Timeline";

function MainPage() {
  return (
    <div className="container mx-auto px-4 py-8">
      <div className="hero bg-base-200 rounded-box mb-8">
        <div className="hero-content text-center">
          <div className="max-w-4xl">
            <h1 className="text-5xl font-bold mb-6">EndoInsight AI</h1>
            <p className="text-2xl mb-4 text-primary">
              AI-Powered Cholecystectomy Surgeries Video Analysis and Explanation System
            </p>
            <p className="text-lg mb-4 italic">
              Revolutionizing surgical education and analysis through advanced AI technology
            </p>
            <p className="text-base">
              EndoInsight AI combines cutting-edge computer vision and natural language processing to provide 
              detailed, expert-level analysis of cholecystectomy (gallbladder removal) surgery videos. Our system 
              offers valuable insights for medical students, surgeons, and healthcare professionals, enhancing 
              understanding of surgical techniques and anatomical structures.
            </p>
          </div>
        </div>
      </div>
      
      <div className="grid md:grid-cols-2 gap-8">
        <div className="card bg-base-100 shadow-xl">
          <div className="card-body flex flex-col items-center">
            <h2 className="card-title text-2xl mb-4 justify-center underline">How It Works</h2>
            <Timeline />
          </div>
        </div>
        
        <div className="card bg-base-100 shadow-xl">
          <div className="card-body">
            <h2 className="card-title text-2xl mb-4 justify-center underline">Try it out now</h2>
            <p className="mb-4">Experience the power of EndoInsight AI firsthand. Upload your cholecystectomy video for instant analysis.</p>
            <div className="form-control">
              <label className="label">
                <span className="label-text">Upload your video (MP4 or MOV, max 800MB)</span>
              </label>
              <input type="file" className="file-input file-input-bordered file-input-primary w-full" accept=".mp4,.mov" />
            </div>
            <div className="card-actions justify-end mt-4">
              <button className="btn btn-primary">Analyze Video</button>
            </div>
          </div>
        </div>
      </div>
      
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