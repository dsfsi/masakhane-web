import React from 'react';
import { useState, useLayoutEffect,useRef, useEffect} from 'react';
import { Container, Row, Col, Form, Button, Modal, Toast, OverlayTrigger, Tooltip } from 'react-bootstrap';
import {CopyToClipboard} from 'react-copy-to-clipboard';

import MultiStepForm from './multiStepForm';

const MIN_TEXTAREA_HEIGHT = 200;

export default function TranslateCard() {
    const [input, setText] = useState("");
    const [translation, setTranslation] = useState('...');
    const [srcLanguages, setSrcLanguages] = useState([]);
    const [tgtLanguages, setTgtLanguages] = useState([]);
    const [show, setShow] = useState(false);
    const [src_lang, setSrc_Lang] = useState('English');
    const [tgt_lang, setTgt_Lang] = useState('Swahili');
    const [feedBackForm, setFeedBackForm] = useState({});
    const textareaRef = useRef(null);
    const textareaRef2= useRef(null);
    const [feedbackToken, setFeedbackToken] = useState(
        localStorage.getItem('feedbackToken') || ''
    );

    const [copySuccess, setCopySuccess] = useState('');
    const [showToast, setShowToast] = useState('');

    const handleClose = () => setShow(false);
    const handleShow = () => setShow(true);

    const copyToClipboard = () => {
        setCopySuccess('Translation Copied!');
        setShowToast(true);
    };

    const handleChangeSrc_Lang= (e) => {
        //localstorage
        localStorage.setItem('src_lang', e.target.value);

        //set state
        setSrc_Lang(e.target.value);
        
    };

    const handleChangeTgt_Lang = (e) => {
        //localstorage
        localStorage.setItem('tgt_lang', e.target.value);

        //set state
        setTgt_Lang(e.target.value);

        // console.log(e.target.value)
        
    };

    const handleTranslate = (e) => {
        console.log('translating ..')
        // console.log(src_lang)
        // console.log(tgt_lang)
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
            //   console.log({ data })
            // do something here
            setTranslation(data.output)
          })
    };

    const submitFeedBack = (formData) => {
        // first set state of feedback Form
        setFeedBackForm({...formData});
        // then submit feedback form to db here
        // here's where you write the function to push feedback to backend

        console.log({formData})

        fetch( 
            '/save', 
            {
                method: 'post', 
                // mode: 'no-cors',
                body: JSON.stringify({
                    src_lang: formData.src_lang,
                    tgt_lang: formData.tgt_lang,
                    accurate_translation:  formData.accurate_translation,
                    know_src_lang: formData.know_src_lang,
                    know_tgt_lang:  formData.know_tgt_lang,
                    own_translation: formData.own_translation,
                    text:  formData.text,
                    translation: formData.translation,
                    understand_translation: formData.understand_translation,
                    feedbackToken: formData.feedbackToken
            }),
                headers: {
                    'Content-Type': 'application/json'
                  },
                // credentials: 'same-origin',
            })
          .then(res => res.json())
          .then(data => {
            //console.log({data})
            // do something here
            handleClear()
          })

    }


    const handleClear = () => {
        // clears text part
        setText('');
        // clear translation
        setTranslation('...');
    }

    useLayoutEffect(() => {
        // Reset height - important to shrink on delete
        textareaRef.current.style.height = "inherit";
        // Set height
        textareaRef.current.style.height = `${Math.max(
          textareaRef.current.scrollHeight,
          MIN_TEXTAREA_HEIGHT
        )}px`;
      }, [input]);

    useLayoutEffect(() => {
        // Reset height - important to shrink on delete
        textareaRef2.current.style.height = "inherit";
        // Set height
        textareaRef2.current.style.height = `${Math.max(
          textareaRef2.current.scrollHeight,
          MIN_TEXTAREA_HEIGHT
        )}px`;
      }, [input]);

    //   console.log({feedbackToken});
    //   console.log({tgt_lang});

    // console.log({feedbackToken});

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
    // console.log(srcLanguages)
    // console.log(tgtLanguages)

    return (
        <Container className="border">
            
            <Modal 
                scrollable={true} 
                show={show} 
                onHide={handleClose} 
                centered 
                size="lg"
            >
                <Modal.Header closeButton style={{backgroundColor:'#F2F0E9'}}>
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
                        setFeedbackToken={setFeedbackToken}
                        feedbackToken={feedbackToken}
                    />
                </Modal.Body>
            </Modal>

            <Row className="header" style={{ backgroundColor: 'aliceblue', height: 60, fontSize: '1rem', padding: '0.5rem 0.5rem' }}>
                <Col className="border-right" style={{marginBottom: 10}}>
                    <Row>
                        <Col md={6} xs={12}>
                            <Form inline>
                                <Form.Group controlId="fromform">
                                    <Form.Label>From: </Form.Label>
                                    <Form.Control value={src_lang} style={{ border: 0, marginLeft: 10 }} as="select" size="sm" custom onChange={handleChangeSrc_Lang}>
                                    {
                                        srcLanguages.map((option, index) => {
                                        return (<option key={index} value={option.name}>{option.name}</option>)
                                        })
                                    }
                                    </Form.Control>
                                </Form.Group>
                            </Form>
                        </Col>
                        {/* <Col className="d-none d-sm-block">
                             <Row>
                            {
                                srcLanguages.length > 1 && srcLanguages
                                .filter(x => x.value !== src_lang)
                                .slice(0, 2)
                                .map((option, index) => {
                                return (
                                    <Button key={option.id} variant="light" size="sm" onClick={() => setSrc_Lang(option.name)}>{option.name}</Button>                                   )
                                })
                            }
                            </Row>
                        </Col> */}
                    </Row>
                </Col>
                <Col style={{ marginLeft: '15px' }}>
                    <Row>
                        <Col md={6} xs={12}>
                            <Form inline>
                                <Form.Group controlId="fromform" as={Row}>
                                <Form.Label>To: </Form.Label>
                                    <Form.Control md={6} xs={12} value={tgt_lang} style={{ border: 0, marginLeft: 10 }} as="select" size="sm" custom onChange={handleChangeTgt_Lang}>
                                    {
                                        tgtLanguages.map((option, index) => {
                                        return (<option key={index} value={option.name}>{option.name}</option>)
                                        })
                                    }
                                    </Form.Control>
                                </Form.Group>
                            </Form>
                        </Col>
                        {/* <Col className="d-none d-sm-block">
                            <Row>
                            {
                                tgtLanguages.length > 1 && tgtLanguages
                                .filter(x => x.value !== tgt_lang)
                                .slice(0, 2)
                                .map((option, index) => {
                                return (
                                    <Button key={option.id} variant="light" size="sm" onClick={() => setTgt_Lang(option.name)}>{option.name}</Button>                                   )
                                })
                            }
                            </Row>
                        </Col> */}
                    </Row>
                </Col>
            </Row>
            <Row style={{ minHeight: '250px', marginTop: '20px' }}>
                <Col md={6} xs={12} className="ml-1" style={{ paddingTop: '20px', paddingBottom: '20px', marginLeft: '10px' }}>
                    <Form>
                        <Form.Group controlId="Form.ControlTextarea">
                            <Form.Control 
                                as="textarea"
                                placeholder="Enter Text" 
                                rows="3" 
                                name="text"
                                ref={textareaRef}
                                style={{ fontSize: 24, minHeight: MIN_TEXTAREA_HEIGHT, resize: 'none' }} 
                                value={input}
                                onChange={e => setText(e.target.value)}
                            />
                        </Form.Group>
                    </Form>
                    
                    <Row>
                        <Col md={10} xs={10}>
                            <Button variant="primary" style={{ marginBottom: 10 }} onClick={handleTranslate}>Translate</Button>
                        </Col>
                        <Col md={2} xs={2} lg="2">
                            <Button style = {{color:'grey'}} variant = 'link' size="sm" onClick={handleClear}><i className="fas fa-times"></i></Button>{' '}
                        </Col>
                    </Row>
                </Col>
                <Col style={{ paddingTop: '20px', paddingBottom: '20px' }}>
                    <Form>
                        <Form.Group controlId="Form.ControlTextarea2">
                            <Form.Control 
                                controlid="translation"
                                as="textarea"
                                placeholder="..." 
                                rows="3" 
                                name="text"
                                ref={textareaRef2}
                                style={{ fontSize: 24, minHeight: MIN_TEXTAREA_HEIGHT, resize: 'none' }} 
                                value={translation}
                                readOnly
                                isInvalid={!translation}
                                // onChange={e => setText(e.target.value)}
                                // autoFocus={showToast}
                            />
                            {!translation && (
                                <Form.Control.Feedback type="invalid">
                                    Sorry, there’s no translation for that phrase.
                                </Form.Control.Feedback>
                            )}
                        </Form.Group>
                    </Form>
                    
                    <Row>
                        <Col md={10} xs={10}>
                            <Button variant="light" size = 'sm' style={{ bottom: '10px' }} onClick={handleShow}>Give Feedback on Translation</Button>
                        </Col>
                        <Col md={2} xs={2} lg="2">
                            <OverlayTrigger
                                placement='top'
                                overlay={
                                <Tooltip id={'tooltip-top'}>
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
                    <Toast.Body style={{color: 'black'}}>{copySuccess}</Toast.Body>
                </Toast>
            </div>
        </Container>
    )
}