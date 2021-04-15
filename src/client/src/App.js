import {
  BrowserRouter as Router,
  Switch,
  Route
} from "react-router-dom";
import { Navbar, Nav, Container, Jumbotron, Image, Row, Col } from 'react-bootstrap'

import Home from './pages/Home';
import About from './pages/About';
import FAQPage from './pages/Faq';
import image from './images/masakhane-border.png';


function App() {
  return (
    <Router>
      <div>
        <Navbar style={{ backgroundColor: '#F2F0E9', width: '100%' }} >
          <Navbar.Brand href="#home" variant="dark" style={{ fontFamily: 'lato', color: 'grey'}}>Masakhane</Navbar.Brand>
          <Navbar.Toggle aria-controls="basic-navbar-nav" />
          <Navbar.Collapse id="basic-navbar-nav" className="justify-content-start">
            <Nav className="ml-auto">
            <Nav.Link href="/">Home</Nav.Link>
                <Nav.Link href="/about">About</Nav.Link>
                <Nav.Link href="/faq">FAQ</Nav.Link>
            </Nav>
          </Navbar.Collapse>
        </Navbar>
<<<<<<< HEAD
        <Jumbotron xs={12} style={{ backgroundColor: '#F2F0E9', paddingTop: '50px', paddingBottom: '50px',backgroundSize: 'cover', backgroundSize: 'cover'}} fluid>
          <Container style={{display:'flex', flexDirection:'row', alignItems:'center', justifyContent:'center'}}>
            <Image src={image}  className="d-none d-sm-block" width='240' height='250' roundedCircle style={{position:"absolute", left:0, right:0}}/>
            <Row xs={12} md={8} style={{display:'flex', flexDirection:'column' ,justifyContent:'center', alignItems:'center'}}>
=======
        {/* <Jumbotron xs={12} style={{ backgroundColor: '#F2F0E9'}} fluid>
          <Container>
            <Row>
              <Col md={4} className="d-none d-sm-block">
                <Image src={image} width='200' height='220' roundedCircle />
              </Col>
              <Col xs={12} md={8} style={{ justifyContent: 'center'}}>
                <h1 style={{ fontFamily: 'lato, sans-serif', fontWeight: 'lighter', fontSize: 80 }}>Masakhane</h1>
                <p>Machine translation service for African languages</p>
              </Col>
            </Row>
          </Container>
        </Jumbotron> */}
        
        <Jumbotron xs = {12} style={{ backgroundColor: '#F2F0E9', paddingTop: '50px', paddingBottom: '50px',backgroundSize: 'cover', backgroundSize: 'cover'}} fluid>
          <Container style={{display:'flex', flexDirection:'row', alignItems:'center', justifyContent:'center'}}>
            <Image className="d-none d-sm-block" src={image} width='240' height='250' roundedCircle style={{position:"absolute", left:0, right:0}}/>
            <Row style={{display:'flex', flexDirection:'column' ,justifyContent:'center', alignItems:'center'}}>
>>>>>>> master
              <h1 style={{ fontFamily: 'lato, sans-serif', fontWeight: 'lighter', fontSize: 80 }}>Masakhane</h1>
              <p>Machine Translation service for African languages</p>
            </Row>
          </Container>
        </Jumbotron>

        <Switch>
            <Route exact path="/">
              <Home />
            </Route>
            <Route path="/about">
              <About />
            </Route>
            <Route path="/faq">
              <FAQPage />
            </Route>
          </Switch>
        {/* <Container className="my-4">
          <br />
          <br />
          <TranslateCard />
          <br />
          <p style={{fontSize: 12, color: 'gray'}}>This is a community research project. Read more about it <span style={{color: 'blue'}}>here</span></p>
        </Container> */}
      </div>
    </Router>
  );
}

export default App;
