class OpenDnD extends React.Component {
    constructor(props) {
        super();
        this.state = {
            page: 'login',
            user: {
                uid: null,
                username: null,
                token: null
            }
        }
    }

    validate = () => {
        let username = document.getElementById("email").value;
        let password = document.getElementById("password").value;
        let data = new FormData();
        data.append("email", username);
        data.append("password", password);
        //Send the request
        fetch("/api/login", {
            "method": "POST",
            "body": data
        })
            .then(res => res.json())
            .then((result) => {
                if (result.result === "failure") {
                    document.getElementById("usernamelabel").innerHTML = result.desc;
                } else if (result.result === "success") {
                    let token = result.token;
                    let user_id = result.uid;
                    let username = result.username;
                    this.setState({user: {uid: user_id, token: token, username: username}, page: 'dashboard'})
                }
            });
    }

    signup = () => {
        console.log("Signup");
        let emailreg = document.getElementById("emailreg").value;
        let passwordreg = document.getElementById("passwordreg").value;
        let usernamereg = document.getElementById("usernamereg").value;
        if (emailreg === "" || passwordreg === "" || usernamereg === "") {
            document.getElementById("emailreg").value = "One or more fields are empty. Retry.";
            return;
        }
        let data = new FormData();
        data.append("email", emailreg);
        data.append("password", passwordreg);
        data.append("username", usernamereg)
        fetch("/api/register", {
            "method": "POST",
            "body": data
        })
            .then(res => res.json())
            .then((result) => {
                if (result.result === "failure") {
                    console.log("Error")
                    document.getElementById("emailreg").value = result.desc;
                } else if (result.result === "success") {
                    console.log("yay")
                    document.getElementById("register").innerHTML = "";
                }
            });
    }

    render() {
        if (this.state.page === 'login') {
            return <Login loginFunc={this.validate} signupFunc={this.signup}></Login>
        } else if (this.state.page === 'dashboard') {
            return <Dashboard token={this.state.user.token} uid={this.state.user.uid}></Dashboard>
        }
        return <div>You ended up in an empty demiplane. It sucks, doesn't it?</div>
    }


}

class Login extends React.Component {
    constructor(props) {
        super(props);
    }

    render() {
        return (
            <div className="login-container">
                <br></br>
                <div className="container">
                    <div className="row">
                        <div className="col-md-6">
                            <div className="jumbotron trasparent">
                                <h1 className="display-3">OpenDnD</h1>
                                <p>Please login to use this website.</p>
                                <div>
                                    <div className="form-group">
                                        <label htmlFor="email" id="usernamelabel">Email</label>
                                        <input type="email" className="form-control" id="email"
                                               aria-describedby="emailHelp"
                                               placeholder="Enter your email" name="email"/>
                                    </div>
                                    <div className="form-group">
                                        <label htmlFor="password">Password</label>
                                        <input type="password" className="form-control" id="password"
                                               placeholder="Password"
                                               name="password"/>
                                    </div>
                                    <button className="btn btn-primary" onClick={this.props.loginFunc}>Login
                                    </button>
                                </div>
                            </div>
                        </div>
                        <div className="col-md-6 white" id="register">
                            <h1 className="display-3"></h1>
                            <p>You don't have an account? Register now!</p>
                            <div>
                                <div className="form-group">
                                    <label htmlFor="emailreg" id="emailabelreg">Email</label>
                                    <input type="email" className="form-control" id="emailreg"
                                           aria-describedby="emailHelp"
                                           placeholder="Enter your email" name="emailreg"/>
                                </div>
                                <div className="form-group">
                                    <label htmlFor="usernamereg" id="usernamelabelreg">Username</label>
                                    <input type="text" className="form-control" id="usernamereg"
                                           aria-describedby="emailHelp"
                                           placeholder="Enter your username" name="usernamereg"/>
                                </div>
                                <div className="form-group">
                                    <label htmlFor="passwordreg">Password</label>
                                    <input type="password" className="form-control" id="passwordreg"
                                           placeholder="Password"
                                           name="passwordreg"/>
                                </div>
                                <button className="btn btn-primary" onClick={this.props.signupFunc}>Sign up
                                </button>
                            </div>
                        </div>
                    </div>
                    <div className="credits">
                        OpenDnD is a WebApplication developed with passion by Fermitech Softworks.
                    </div>
                </div>
            </div>
        )
    }
}

class Dashboard extends React.Component {
    constructor(props) {
        super(props);
        this.state = {campaigns: [{title: null, owner: {uid: null, username: null},cid: null}
    ]
    }
        ;
    }

    gatherCampaignData() {
        let data = new FormData();
        data.append("token", this.props.token);
        data.append("uid", this.props.uid);
        fetch("/api/get_campaigns", {
            "method": "POST",
            "body": data
        })
            .then(res => res.json())
            .then((result) => {
                if (result.result === "failure") {
                    console.log(result.desc)
                } else if (result.result === "success") {
                    this.setState({campaigns: result.campaigns})
                }
            });
    }

    componentDidMount() {
        this.gatherCampaignData()
    }

    render() {
        let campaigns = this.state.campaigns.map((item) => {
            return (
                <div key={item.cid}>{item.title}</div>
            )
        })
        return (
            <div className="dashboard-container">
                <br></br>
                <div className="container">
                    <div className="jumbotron trasparent">
                        {campaigns}
                    </div>
                </div>

            </div>
        )
    }
}

ReactDOM.render(
    <div id="react-app">
        <OpenDnD></OpenDnD>
    </div>,
    document.getElementById('react-app')
);