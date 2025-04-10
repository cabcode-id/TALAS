import { Routes, Route} from 'react-router-dom';
import MainLayout from "./layouts/MainLayout";
import AuthLayout from "./layouts/AuthLayout";
import HomePage from './pages/HomePage';
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';
import NewsPage from './pages/NewsPage';
import SubscriptionPage from './pages/SubscriptionPage';
import AboutUsPage from './pages/AboutUsPage';
import SearchPage from './pages/SearchPage';

const App = () => {
  return (
    <Routes>
      <Route path="/home" element={<MainLayout />}>
        <Route index element={<HomePage />} />
      </Route>

      <Route path="/search" element={<MainLayout />}>
        <Route index element={<SearchPage />} />
      </Route>

      <Route path='/login' element={<AuthLayout />}>
        <Route index element={<LoginPage />} />
      </Route>
      <Route path='/register' element={<AuthLayout />}>
        <Route index element={<RegisterPage />} />
      </Route>
      <Route path='/news/detail' element={<MainLayout />}>
        <Route index element={<NewsPage />} />
      </Route>    
      <Route path='/subscription' element={<MainLayout />}>
        <Route index element={<SubscriptionPage />} />
      </Route>

      <Route path='/about-us' element={<MainLayout />}>
        <Route index element={<AboutUsPage />} />
      </Route>  
    </Routes>
  );
};

export default App;
