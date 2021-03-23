import { useState, useRef, useEffect} from 'react';
import { Container, Row, Col, Form, Button, Modal, Toast, OverlayTrigger, Tooltip } from 'react-bootstrap';
import {CopyToClipboard} from 'react-copy-to-clipboard';

export default function TranslateCard() {
    const [input, setText] = useState("");
    const [translation, setTranslation] = useState("");
    const [srcLanguages, setSrcLanguages] = useState([]);
    const [tgtLanguages, setTgtLanguages] = useState([]);
    const [show, setShow] = useState(false);
    const [src_lang, setSrc_Lang] = useState('English');
    const [tgt_lang, setTgt_Lang] = useState('Swahili');
    const [feedBackForm, setFeedBackForm] = useState({});

    const textAreaRef = useRef(null);
    const [copySuccess, setCopySuccess] = useState('');
    const [showToast, setShowToast] = useState('');

    const handleClose = () => setShow(false);
    const handleShow = () => setShow(true);

    const copyToClipboard = () => {
        setCopySuccess('Translation Copied!');
        setShowToast(true);
    };

    const handleChangeSrc_Lang= (e) => {
        setSrc_Lang(e.target.value);
    };

    const handleChangeTgt_Lang = (e) => {
        setTgt_Lang(e.target.value);
    };

    const handleTranslate = (e) => {
        console.log('translating ..')
        e.preventDefault()
    
        fetch( 
            '/translate', 
            {
                method: 'post', 
                // mode: 'no-cors',
                body: JSON.stringify({input, src_lang, tgt_lang}),
                headers: {
                    'Content-Type': 'application/json'
                  },
                // credentials: 'same-origin',
            })
          .then(res => res.json())
          .then(data => {
              console.log({ data })
            // do something here
            setTranslation(data.output)
          })
    };

    const submitFeedBack = (formData) => {
        // first set state of feedback Form
        setFeedBackForm({...formData});
        // then submit feedback form to db here
        // here's where you write the function to push feedback to backend

    }

    const handleClear = () => {
        // clears text part
        setText('');
        // clear translation
        setTranslation('...');
    }

    let srcLang = [];
    let tgtLang = [];

    useEffect(()=> {
        // define fetch function 
        let src = [];
        let tgt = [];
        const fetchLanguages = async ()=> {
        await fetch( 
            '/translate', 
            {
                method: 'get', 
                headers: {
                    'Content-Type': 'application/json'
                  },
                // credentials: 'same-origin',
            })
          .then(res => res.json())
          .then(data => {
              console.log({ data })
            // do something here
            setSrcLanguages(data.filter(x => x.type == "source"))
            setTgtLanguages(data.filter(x => x.type == "target"))
        
          })
        

        }
        // call fetch function
        fetchLanguages()

    }, [])
    console.log(srcLanguages)
    console.log(tgtLanguages)

    return (
        <Container className="border" style={{borderRadius: '5px'}}>
            <Row className="header" style={{ backgroundColor: 'aliceblue', height: 60, fontSize: '1rem', padding: '1rem 1.5rem'}}>
                <Col className="border-right" style={{marginBottom: 10}}>
                    <Row>
                        <Col>
                            <Form inline>
                                <Form.Group controlId="fromform">
                                <Form.Label>From: </Form.Label>
                                    <Form.Control value={src_lang} style={{ border: 0 }} as="select" size="md" custom onChange={handleChangeSrc_Lang}>
                                    {
                                        srcLanguages.map((option, index) => {
                                        return (<option key={index} value={option.name}>{option.name}</option>)
                                        })
                                    }
                                    </Form.Control>
                                </Form.Group>
                            </Form>
                        </Col>
                        <Col>
                             <Row>
                            {
                                srcLanguages.length > 1 && srcLanguages
                                .filter(x => x.value !== src_lang)
                                .slice(0, 3)
                                .map((option, index) => {
                                return (
                                    <Button key={option.id} variant="light" size="sm" onClick={() => setSrc_Lang(option.name)}>{option.name}</Button>                                   )
                                })
                            }
                            </Row>
                        </Col>
                    </Row>
                </Col>
                <Col style={{ marginLeft: '15px' }}>
                <Row>
                    <Col md={6} xs={12}>
                        <Form inline>
                            <Form.Group controlId="fromform">
                            <Form.Label>To: </Form.Label>
                                <Form.Control value={tgt_lang} style={{ border: 0 }} as="select" size="md" custom onChange={handleChangeTgt_Lang}>
                                {
                                    tgtLanguages.map((option, index) => {
                                    return (<option key={option.id} key={index} value={option.name}>{option.name}</option>)
                                    })
                                }
                                </Form.Control>
                            </Form.Group>
                        </Form>
                    </Col>
                    <Col>
                        <Row>
                        {
                            tgtLanguages.length > 1 && tgtLanguages
                            .filter(x => x.value !== tgt_lang)
                            .slice(0, 3)
                            .map((option, index) => {
                            return (
                                <Button key={option.id} variant="light" size="sm" onClick={() => setTgt_Lang(option.name)}>{option.name}</Button>                                   )
                            })
                        }
                        </Row>
                    </Col>
                </Row>
            </Col>
            
            </Row>
            <Row style={{ minHeight: '15px' }}>
            <Col md={6} xs={12} className="mr-3" style={{ paddingTop: '20px', paddingBottom: '20px', marginLeft: '10px' }}>
                    <Form>
                        <Form.Group controlId="Form.ControlTextarea">
                            <Form.Control 
                                as="textarea"
                                placeholder="Enter Text" 
                                rows="3" 
                                name="text"
                                style={{ height: '200px', fontSize: 20, font:'lato, sans-serif' }} 
                                value={input}
                                onChange={e => setText(e.target.value)}
                            />
                        </Form.Group>
                    </Form>
                    
                    <Row>
                        <Col md={10} xs={10}>
                            <Button variant="primary" onClick={handleTranslate}>Translate</Button>
                        </Col>
                        <Col md="auto">{' '}</Col>
                        <Col md={2} xs={2} lg="2">
                            <Button  style = {{color:'grey'}} variant = 'link' size="sm" onClick={handleClear}>clear</Button>{' '}
                        </Col>
                    </Row>
                </Col>
                <Col className="ml-3" style={{ paddingTop: '20px', paddingBottom: '20px' }}>
                    <Form>
                        <Form.Group controlId="Form.ControlTextarea2">
                            <Form.Control 
                                as="textarea"
                                // ref={textAreaRef}
                                placeholder="..." 
                                rows="3" 
                                name="text"
                                style={{ height: '200px', fontSize: 20 }} 
                                value={translation}
                                readOnly
                                // onChange={e => setText(e.target.value)}
                                // autoFocus={showToast}
                            />
                        </Form.Group>
                    </Form>
                    
                    <Row>
                        <Col>
                            {' '}
                        </Col>
                        <Col md="auto">{' '}</Col>
                        <Col xs lg="2">
                        <OverlayTrigger
                                placement='top'
                                overlay={
                                <Tooltip id={'tooltip-top'} >
                                    Copy <strong>Translation</strong>.
                                </Tooltip>
                                }
                            >
                                <CopyToClipboard text={translation} onCopy={copyToClipboard}>
                                    <Button variant="light" size="sm"><i className="fa fa-copy"></i></Button>
                                </CopyToClipboard>
                            </OverlayTrigger>
                        </Col>
                    </Row>
                </Col>
            </Row>

            <div aria-live="polite" aria-atomic="true" style={{ position: 'relative' }}>
                <Toast
                    onClose={() => setShowToast(false)} 
                    show={showToast} 
                    delay={3000} 
                    autohide
                    style={{
                        position: 'absolute',
                        bottom: 0,
                        left: 0
                    }}
                >
                    <Toast.Body style={{color: 'green'}}>{copySuccess}</Toast.Body>
                </Toast>
            </div>
        </Container>
    )
}