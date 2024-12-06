import { useState, useEffect } from 'react';
import './App.css';

export default function App() {
  const [isDarkMode, setIsDarkMode] = useState(false);

  // Fungsi untuk toggle Dark Mode
  const toggleDarkMode = () => {
    setIsDarkMode((prevMode) => !prevMode);

    // Tambahkan atau hapus kelas "dark-mode" di elemen body
    if (!isDarkMode) {
      document.body.classList.add("dark-mode");
    } else {
      document.body.classList.remove("dark-mode");
    }
  };

  return (
    <>
      <Navbar toggleDarkMode={toggleDarkMode} isDarkMode={isDarkMode} />
      <News />
      
    </>
  );
}

// eslint-disable-next-line react/prop-types
function Navbar({ toggleDarkMode, isDarkMode }) {
  return (
    <nav className="navbar">
      <Logo />
      <Search />
      <Links />
      <Button />
      <div className="toggle-container">
        {/* Tombol untuk Dark Mode */}
        <button onClick={toggleDarkMode} className="toggle-container">
          {isDarkMode ? "L" : "D"}
        </button>
        {/* <h3 className='teks-dark'>Dark Mode</h3> */}
      </div>
      
    </nav>
  );
}

function Logo() {
  return (
    <div className="logo-container">
      <img src="/Logo.png" alt="Logo" className="logo" />
      <img src="/Title.png" alt="Title" className="title" />
    </div>
  );
}

function Search() {
  const [query, setQuery] = useState('');
  return (
    <div className="search-bar">
      <input
        type="text"
        placeholder="Search..."
        className="search-bar"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
      />
    </div>
  );
}

function Links() {
  return (
    <div>
      <ul className="links">
        <li><a href="#home">Home</a></li>
        <li><a href="#internasional">Internasional</a></li>
        <li><a href="#nasional">Nasional</a></li>
        <li><a href="#otomotif">Otomotif</a></li>
        <li><a href="#kesehatan">Kesehatan</a></li>
        <li><a href="#ekonomi">Ekonomi</a></li>
        <li><a href="#finansial">Finansial</a></li>
        <li><a href="#teknologi">Teknologi</a></li>
        <li><a href="#lifestyle">Lifestyle</a></li>
        <li><a href="#politik">Politik</a></li>
        <li><a href="#hiburan">Hiburan</a></li>
        <li><a href="#olahraga">Olahraga</a></li>
      </ul>
    </div>
  );
}

function Button() {
  return (
    <div className="auth-buttons">
      <button className="btn login-btn">Login</button>
      <button className="btn subscribe-btn">Subscribe</button>
    </div>
  );
}



// berita LAyout
function News() {
  const endpoint = 'http://localhost:3000/article';
  const [message, setMessage] = useState('');

  const fetchData = async () => {
    try {
      const response = await fetch(endpoint);
      const data = await response.json();
      setMessage(data.message); // Update state dengan pesan dari API
    } catch (error) {
      console.error('Error fetching data:', error);
    }
  };

  useEffect(() => {
    fetchData(); // Memanggil fungsi fetchData
  }, []); // Dependency array kosong untuk memastikan ini hanya dijalankan sekali

  return (
    <div>
      <h1>{message}</h1>
      <Headline/>
      <NewsLayout/>
    </div>
  );
}



// bagian berita utama/news page

function NewsPage() {
  return (
    <div className="left">
      {/* <AdditionalNews /> */}
    <div className='left-section'>
      <h1 className='h1'>Berita Utama</h1>
      <div className='card'>
      <section className='article'>
        <img src="https://awsimages.detik.net.id/community/media/visual/2024/11/21/menteri-bumn-sekaligus-ketua-umum-pssi-erick-thohir-saat-ditemui-di-bandara-internasional-i-gusti-ngurah-rai-badung-bali-kamis_169.jpeg?w=700&q=90" alt="tech" className='img' />
          <article>
            <p className='news-title'> <a href="https://finance.detik.com/berita-ekonomi-bisnis/d-7651274/erick-thohir-sebut-2-juta-orang-ri-berobat-ke-luar-negeri-devisa-rp-90-t-hilang">
            Erick Thohir Sebut 2 Juta Orang RI Berobat ke Luar Negeri, Devisa Rp 90 T Hilang </a>
            </p>
          </article>
        
      </section>
      </div>
    </div>

  <div className="left-section">
  <div className='card'>
  <section className='article'>
        <img src="https://awsimages.detik.net.id/community/media/visual/2024/11/21/menteri-bumn-sekaligus-ketua-umum-pssi-erick-thohir-saat-ditemui-di-bandara-internasional-i-gusti-ngurah-rai-badung-bali-kamis_169.jpeg?w=700&q=90" alt="tech" className='img' />
          <article>
            <p className='news-title'> <a href="https://finance.detik.com/berita-ekonomi-bisnis/d-7651274/erick-thohir-sebut-2-juta-orang-ri-berobat-ke-luar-negeri-devisa-rp-90-t-hilang">
            Erick Thohir Sebut 2 Juta Orang RI Berobat ke Luar Negeri, Devisa Rp 90 T Hilang </a>
            </p>
          </article>
        
      </section>
    </div>
  </div>

  <div className="left-section">
  <div className='card'>
  <section className='article'>
        <img src="https://awsimages.detik.net.id/community/media/visual/2024/11/21/menteri-bumn-sekaligus-ketua-umum-pssi-erick-thohir-saat-ditemui-di-bandara-internasional-i-gusti-ngurah-rai-badung-bali-kamis_169.jpeg?w=700&q=90" alt="tech" className='img' />
          <article>
            <p className='news-title'> <a href="https://finance.detik.com/berita-ekonomi-bisnis/d-7651274/erick-thohir-sebut-2-juta-orang-ri-berobat-ke-luar-negeri-devisa-rp-90-t-hilang">
            Erick Thohir Sebut 2 Juta Orang RI Berobat ke Luar Negeri, Devisa Rp 90 T Hilang </a>
            </p>
          </article>
        
      </section>
    </div>
  </div>

  <div className="left-section">
  <div className='card'>
  <section className='article'>
        <img src="https://awsimages.detik.net.id/community/media/visual/2024/11/21/menteri-bumn-sekaligus-ketua-umum-pssi-erick-thohir-saat-ditemui-di-bandara-internasional-i-gusti-ngurah-rai-badung-bali-kamis_169.jpeg?w=700&q=90" alt="tech" className='img' />
          <article>
            <p className='news-title'> <a href="https://finance.detik.com/berita-ekonomi-bisnis/d-7651274/erick-thohir-sebut-2-juta-orang-ri-berobat-ke-luar-negeri-devisa-rp-90-t-hilang">
            Erick Thohir Sebut 2 Juta Orang RI Berobat ke Luar Negeri, Devisa Rp 90 T Hilang </a>
            </p>
          </article>
        
      </section>
    </div>
  </div>

  <div className="left-section">
  <div className='card'>
  <section className='article'>
        <img src="https://awsimages.detik.net.id/community/media/visual/2024/11/21/menteri-bumn-sekaligus-ketua-umum-pssi-erick-thohir-saat-ditemui-di-bandara-internasional-i-gusti-ngurah-rai-badung-bali-kamis_169.jpeg?w=700&q=90" alt="tech" className='img' />
          <article>
            <p className='news-title'> <a href="https://finance.detik.com/berita-ekonomi-bisnis/d-7651274/erick-thohir-sebut-2-juta-orang-ri-berobat-ke-luar-negeri-devisa-rp-90-t-hilang">
            Erick Thohir Sebut 2 Juta Orang RI Berobat ke Luar Negeri, Devisa Rp 90 T Hilang </a>
            </p>
          </article>
        
      </section>
    </div>
  </div>

  <div className="left-section">
  <div className='card'>
  <section className='article'>
        <img src="https://awsimages.detik.net.id/community/media/visual/2024/11/21/menteri-bumn-sekaligus-ketua-umum-pssi-erick-thohir-saat-ditemui-di-bandara-internasional-i-gusti-ngurah-rai-badung-bali-kamis_169.jpeg?w=700&q=90" alt="tech" className='img' />
          <article>
            <p className='news-title'> <a href="https://finance.detik.com/berita-ekonomi-bisnis/d-7651274/erick-thohir-sebut-2-juta-orang-ri-berobat-ke-luar-negeri-devisa-rp-90-t-hilang">
            Erick Thohir Sebut 2 Juta Orang RI Berobat ke Luar Negeri, Devisa Rp 90 T Hilang </a>
            </p>
          </article>
        
      </section>
      </div>
  </div>
  </div>
  )}
        

// berita tengah

function Headline() {
  return (
    <div className="headline">
    <div className='center-section'>
      {/* <AdditionalNews /> */}
      <section >
          <article>
            <h1 className='title-headline'> <a href="https://finance.detik.com/berita-ekonomi-bisnis/d-7651274/erick-thohir-sebut-2-juta-orang-ri-berobat-ke-luar-negeri-devisa-rp-90-t-hilang">
            Erick Thohir Sebut 2 Juta Orang RI Berobat ke Luar Negeri, Devisa Rp 90 T Hilang </a></h1>
            <img src="https://awsimages.detik.net.id/community/media/visual/2024/11/21/menteri-bumn-sekaligus-ketua-umum-pssi-erick-thohir-saat-ditemui-di-bandara-internasional-i-gusti-ngurah-rai-badung-bali-kamis_169.jpeg?w=700&q=90" alt="tech" className='img-headline' />
          </article>
        </section>
    </div>

    <div className='center-section'>
    <h1 className='h1'>Berita Utama</h1>
      <section className='article'>
      <img src="https://awsimages.detik.net.id/community/media/visual/2024/11/21/menteri-bumn-sekaligus-ketua-umum-pssi-erick-thohir-saat-ditemui-di-bandara-internasional-i-gusti-ngurah-rai-badung-bali-kamis_169.jpeg?w=700&q=90" alt="tech" className='img' />
      <article>
            <p className='news-title'> <a href="https://finance.detik.com/berita-ekonomi-bisnis/d-7651274/erick-thohir-sebut-2-juta-orang-ri-berobat-ke-luar-negeri-devisa-rp-90-t-hilang">
            Erick Thohir Sebut 2 Juta Orang RI Berobat ke Luar Negeri, Devisa Rp 90 T Hilang </a>
            </p>
          </article>
        
      </section>
    </div>

    <div className='center-section'>
    <section className='article'>
      <img src="https://awsimages.detik.net.id/community/media/visual/2024/11/21/menteri-bumn-sekaligus-ketua-umum-pssi-erick-thohir-saat-ditemui-di-bandara-internasional-i-gusti-ngurah-rai-badung-bali-kamis_169.jpeg?w=700&q=90" alt="tech" className='img' />
      <article>
            <p className='news-title'> <a href="https://finance.detik.com/berita-ekonomi-bisnis/d-7651274/erick-thohir-sebut-2-juta-orang-ri-berobat-ke-luar-negeri-devisa-rp-90-t-hilang">
            Erick Thohir Sebut 2 Juta Orang RI Berobat ke Luar Negeri, Devisa Rp 90 T Hilang </a>
            </p>
          </article>
        
      </section>
    </div>

    <div className='center-section'>
    <section className='article'>
      <img src="https://awsimages.detik.net.id/community/media/visual/2024/11/21/menteri-bumn-sekaligus-ketua-umum-pssi-erick-thohir-saat-ditemui-di-bandara-internasional-i-gusti-ngurah-rai-badung-bali-kamis_169.jpeg?w=700&q=90" alt="tech" className='img' />
      <article>
            <p className='news-title'> <a href="https://finance.detik.com/berita-ekonomi-bisnis/d-7651274/erick-thohir-sebut-2-juta-orang-ri-berobat-ke-luar-negeri-devisa-rp-90-t-hilang">
            Erick Thohir Sebut 2 Juta Orang RI Berobat ke Luar Negeri, Devisa Rp 90 T Hilang </a>
            </p>
          </article>
        
      </section>
    </div>

    <div className='center-section'>
    <section className='article'>
      <img src="https://awsimages.detik.net.id/community/media/visual/2024/11/21/menteri-bumn-sekaligus-ketua-umum-pssi-erick-thohir-saat-ditemui-di-bandara-internasional-i-gusti-ngurah-rai-badung-bali-kamis_169.jpeg?w=700&q=90" alt="tech" className='img' />
      <article>
            <p className='news-title'> <a href="https://finance.detik.com/berita-ekonomi-bisnis/d-7651274/erick-thohir-sebut-2-juta-orang-ri-berobat-ke-luar-negeri-devisa-rp-90-t-hilang">
            Erick Thohir Sebut 2 Juta Orang RI Berobat ke Luar Negeri, Devisa Rp 90 T Hilang </a>
            </p>
          </article>
        
      </section>
    </div>

    </div>
  )
}


function NewsLayout() {
  return (
    <div className="news-layout">
      <div className='right-section'>
      <section >
          <article>
          <h1 className='h1'>Talas Blind Zone </h1>
            <img src="https://awsimages.detik.net.id/community/media/visual/2024/11/21/menteri-bumn-sekaligus-ketua-umum-pssi-erick-thohir-saat-ditemui-di-bandara-internasional-i-gusti-ngurah-rai-badung-bali-kamis_169.jpeg?w=700&q=90" alt="tech" className='img' />
            <p> <a href="https://finance.detik.com/berita-ekonomi-bisnis/d-7651274/erick-thohir-sebut-2-juta-orang-ri-berobat-ke-luar-negeri-devisa-rp-90-t-hilang">
            Erick Thohir Sebut 2 Juta Orang RI Berobat ke Luar Negeri, Devisa Rp 90 T Hilang 
            </a> </p>
            
          </article>
        </section>
    </div>
    </div>
  )
}








  
