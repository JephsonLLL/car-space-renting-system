import Site from './components/Site';
import useToken from './components/useToken';
import Login from './pages/Login';

function App() {
  const { token, setToken } = useToken();
  if(!token && window.location.pathname !== '/register') {
   return <Login setToken={setToken} />
  }
  return (
   <Site />
  );
}

export default App;