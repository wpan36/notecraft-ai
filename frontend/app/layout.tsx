import './globals.css';
import Link from 'next/link';

export const metadata = {
  title: 'NoteCraft.AI',
  description: 'Simple AI note-taking frontend'
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <header className="nc-header">
          <div className="nc-container">
            <Link href="/" className="brand">NoteCraft.AI</Link>
            <nav className="nav">
              <Link href="/">Home</Link>
              <Link href="/search">Search</Link>
            </nav>
          </div>
        </header>
        <main className="nc-container">{children}</main>
        <footer className="nc-footer">
          <div className="nc-container">© 2025 NoteCraft.AI</div>
        </footer>
      </body>
    </html>
  );
}
