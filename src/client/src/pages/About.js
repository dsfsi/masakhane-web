import { Container, Card } from 'react-bootstrap'

export default function About() {
    return(
        <div>
            <Container className="my-4">
                <Card style={{ width: '100%' }}>
                    <Card.Body>
                        <Card.Title>About</Card.Title>
                        <Card.Subtitle className="mb-2 text-muted">Masakhane Web</Card.Subtitle>
                        <div>
                            <Card.Text style={{ fontSize: 16, color: 'black' }}>
                            <b>Masakhane Web</b> is an open source online machine translation service for solely African languages.  
                            This project is in line with the works of the <a id='link' href='https://www.masakhane.io/'>Masakhane community</a> .<b> Masakhane</b> meaning ‘we build together’, 
                            is a research effort whose mission is to strengthen and spur NLP research for African languages which is open source and online. 
                            So far, the community has trained translation models for over 38 African languages. As such, this platform aims at hosting the already trained machine translation models from the Masakhane community and allows contributions 
                            from users to create new data for retraining and improving the models.
                            </Card.Text>
                        </div>
                        <div>
                            <Card.Text style={{ fontSize: 16, color: 'black' }}>
                            <br />
                            The Masakhane Web project is led by <a id='link' href='https://dsfsi.github.io/'>Data Science for Social Impact</a> research group at the <a id = 'link' href = 'https://cs.up.ac.za/'>Department of Computer Science</a>, University of Pretoria, South Africa. 
                            </Card.Text>
                            </div>
                            <br/>
                        <div>
                        <Card.Text style={{ fontSize: 16, color: 'black' }}>
                            The feedback mechanism of this project has been approved by the University of Pretoria Faculty of Engineering, <a id='link' href = 'https://www.up.ac.za/faculty-of-engineering-built-environment-it/article/15815/faculty-committee-for-research-ethics-integrity' >Built Environment and Information Technology(EBIT) Research Ethics Committee</a>. 
                            </Card.Text>
                        </div>

                        <br />
                        <div>
                            <Card.Text style={{ fontSize: 16, color: 'black' }}>

                            
                            If you're interested in training a model in your language or to find out more on how you can collaborate and work with Masakhane, please check out their website <a id='link' href='https://www.masakhane.io'>https://www.masakhane.io </a> 
                             or you can reach any of the Masakhane Web contributors in the following ways:
                             </Card.Text>
                        </div>
                        <div>
                            <Card.Text style={{ fontSize: 16, color: 'gray' }}>
                            <br />
                            <br />
                            <span><b>Dr. Vukosi Marivate</b></span>
                            <br />
                            <span><i>vukosi.marivate@cs.up.ac.za</i></span>
                            <br />
                            <a id='link' href= 'https://twitter.com/vukosi'>@vukosi</a>
                            <br />
                            <br />
                            <span><b>Abiodun Modupe</b></span>
                            <br />
                            <span><i>abiodun.modupe@cs.up.ac.za </i></span>
                            <br />
                            <br />
                            <span><b>Salomon Kabongo</b></span>
                            <br />
                            <a id='link' href= 'https://twitter.com/SalomonKabongo'>@SalomonKabongo</a>
                            <br />
                            <br />
                            <span><b>Catherine Gitau</b></span>
                            <br />
                            <a id='link' href= 'https://twitter.com/categitau_'>@categitau_</a>
                            <br />


                            </Card.Text>
                        </div>
                        <br />
                    </Card.Body>
                </Card>
            </Container>
        </div>
    )
}