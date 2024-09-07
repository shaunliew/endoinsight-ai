import { create } from 'zustand';

const useFileStore = create((set) => ({
  file: null,
  error: '',
  isLoading: false,
  analysisResult: null,
  setFile: (file) => set({ file }),
  clearFile: () => set({ file: null }),
  setError: (error) => set({ error }),
  setIsLoading: (isLoading) => set({ isLoading }),
  setAnalysisResult: (result) => set({ analysisResult: result }),
}));

export default useFileStore;