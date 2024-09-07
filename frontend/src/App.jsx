import Footer from './components/Footer';
import Header from './components/Header';
import MainPage from './pages/MainPage';
function App() {
  return (
    <div className="flex flex-col min-h-screen">
    <Header />
    <main className="flex-grow">
    <MainPage />
    </main>
    <Footer />
  </div>
  )
}

export default App
