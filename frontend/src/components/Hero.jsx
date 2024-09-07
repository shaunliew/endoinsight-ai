import AnimatedDrawing from "./AnimatedDrawing";
import TypingText from "./TypingText";
import curveline from "../assets/curveline.svg";
const Hero = () => {
    return (
        <div className="hero bg-base-100 rounded-box mb-8 shadow-xl"
        style={{
    backgroundImage: `url(${curveline})`,
  }}>
        <div className="hero-content text-center">
            
          <div className="max-w-4xl">
            <AnimatedDrawing word = "EndoInsight AI" class = "p-4"/>
            <TypingText text="AI-Powered Cholecystectomy Surgeries Video Analysis and Explanation System" speed={80} fontSize="text-lg" color="text-blue-800" fontStyle="italic" />
            <p className="text-lg mb-4 italic font-bold">
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
    );
  };
  
  export default Hero;