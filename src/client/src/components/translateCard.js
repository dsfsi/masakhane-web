import { useState, useRef } from 'react';
import { Container, Row, Col, Form, Button, Modal, Toast, OverlayTrigger, Tooltip } from 'react-bootstrap';
import {CopyToClipboard} from 'react-copy-to-clipboard';

import MultiStepForm from './multiStepForm';

const sourceLanguages = [
    { id: 1, name: "English", value: 'en' },
];

const targetLanguages = [
    { id: 1, name: "Swahili", value: 'sw' },
    { id: 2, name: "Sesotho", value: 'se' },
    { id: 3, name: "Yoruba", value: 'yo' },
    { id: 4, name: "Twi", value: 'tw' },
];

export default function TranslateCard() {
    const [input, setText] = useState("");
    const [translation, setTranslation] = useState("");
    const [show, setShow] = useState(false);
    const [src_lang, setSrc_Lang] = useState('en');
    const [tgt_lang, setTgt_Lang] = useState('sw');
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

    return (
        <Container className="border">
            <Modal scrollable={true} show={show} onHide={handleClose} centered style={{ maxHeight: '700px' }}>
                <Modal.Header closeButton>
                {/*<Modal.Title>Modal heading</Modal.Title>*/}
                <Col style={{textAlign: 'center'}}>
                    <h4 style={{ fontSize: 14, color: '#717171' }}>GIVE FEEDBACK</h4>
                    <p style={{ fontSize: 11, color: 'gray' }}>We appreciate your feedback and your contribution will help make our translation better.</p>
                </Col>
                </Modal.Header>
                <Modal.Body>
                    <MultiStepForm 
                        src_lang={src_lang} 
                        tgt_lang={tgt_lang} 
                        text={input} 
                        translation={translation} 
                        setShow={setShow}
                        submitFeedBack={submitFeedBack}
                    />
                </Modal.Body>
            </Modal>

            <Row className="header" style={{ backgroundColor: 'aliceblue', height: 60, fontSize: '1rem', padding: '1rem 1.5rem'}}>
                <Col className="border-right">
                    <Row>
                        <Col>
                            <Form inline>
                                <Form.Group controlId="fromform">
                                <Form.Label>From: </Form.Label>
                                    <Form.Control value={src_lang} style={{ border: 0 }} as="select" size="md" custom onChange={handleChangeSrc_Lang}>
                                    {
                                        sourceLanguages.map((option, index) => {
                                        return (<option key={index} value={option.value}>{option.name}</option>)
                                        })
                                    }
                                    </Form.Control>
                                </Form.Group>
                            </Form>
                        </Col>
                        <Col>
                             <Row>
                            {
                                sourceLanguages
                                .filter(x => x.value !== src_lang)
                                .slice(0, 3)
                                .map((option, index) => {
                                return (
                                    <Button key={option.id} variant="light" size="sm" onClick={() => setSrc_Lang(option.value)}>{option.name}</Button>                                   )
                                })
                            }
                            </Row>
                        </Col>
                    </Row>
                </Col>
                <Col className="ml-3">
                <Row>
                    <Col>
                        <Form inline>
                            <Form.Group controlId="fromform">
                            <Form.Label>To: </Form.Label>
                                <Form.Control value={tgt_lang} style={{ border: 0 }} as="select" size="md" custom onChange={handleChangeTgt_Lang}>
                                {
                                    targetLanguages.map((option, index) => {
                                    return (<option key={option.id} key={index} value={option.value}>{option.name}</option>)
                                    })
                                }
                                </Form.Control>
                            </Form.Group>
                        </Form>
                    </Col>
                    <Col>
                        <Row>
                        {
                            targetLanguages
                            .filter(x => x.value !== tgt_lang)
                            .slice(0, 3)
                            .map((option, index) => {
                            return (
                                <Button key={option.id} variant="light" size="sm" onClick={() => setTgt_Lang(option.value)}>{option.name}</Button>                                   )
                            })
                        }
                        </Row>
                    </Col>
                </Row>
                </Col>
            </Row>
            <Row style={{ minHeight: '250px' }}>
                <Col className="border-right" style={{ paddingTop: '20px', paddingBottom: '20px' }}>
                    <Form>
                        <Form.Group controlId="Form.ControlTextarea">
                            <Form.Control 
                                as="textarea"
                                placeholder="Enter Text" 
                                rows="3" 
                                name="text"
                                style={{ height: '200px', fontSize: 24 }} 
                                value={input}
                                onChange={e => setText(e.target.value)}
                            />
                        </Form.Group>
                    </Form>
                    
                    <Row>
                        <Col>
                            <Button variant="outline-primary" onClick={handleTranslate}>Translate</Button>
                        </Col>
                        <Col md="auto">{' '}</Col>
                        <Col xs lg="2">
                            <Button  variant = 'light' size="sm" onClick={() => setText("")}><i className="fas fa-times"></i></Button>{' '}
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
                                style={{ height: '200px', fontSize: 24 }} 
                                value={translation}
                                readOnly
                                // onChange={e => setText(e.target.value)}
                                // autoFocus={showToast}
                            />
                        </Form.Group>
                    </Form>
                    
                    <Row>
                        <Col xs lg="2">
                            <CopyToClipboard text={translation} onCopy={copyToClipboard}>
                                <Button variant = 'light' size="sm"><i className="fa fa-copy"></i></Button>
                            </CopyToClipboard>
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