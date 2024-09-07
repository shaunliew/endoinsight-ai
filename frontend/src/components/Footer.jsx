const Footer = () => {
  return (
    <footer className="footer bg-base-200 text-base-content items-center p-4">
      <aside className="grid-flow-col items-center">
        <p>EndoInsight AI Copyright © {new Date().getFullYear()} - All right reserved</p>
      </aside>
    </footer>
  );
};

export default Footer;