import { create } from 'zustand';

const useFileStore = create((set) => ({
  file: null,
  error: '',
  isLoading: false,
  setFile: (file) => set({ file }),
  clearFile: () => set({ file: null }),
  setError: (error) => set({ error }),
  setIsLoading: (isLoading) => set({ isLoading }),
}));

export default useFileStore;