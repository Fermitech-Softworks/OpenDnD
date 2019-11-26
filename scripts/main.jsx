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

    render() {
        if (this.state.page === 'login') {
            return <Login loginFunc={this.validate}></Login>
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
            <div>
                <div className="row">
                    <div className="col-md-6">
                        <div className="jumbotron">
                            <h1 className="display-3">OpenDnD</h1>
                            <p className="lead"></p>
                            <hr className="my-4"></hr>
                            <p>Please login to use this website.</p>
                            <p className="lead"></p>
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
                                <button className="btn btn-primary" onClick={this.props.loginFunc}>Login</button>
                            </div>
                        </div>
                    </div>
                    <div className="col-md-6">
                        <a href="/signup" type="button" className="btn btn-success btn-lg btn-block">Create an
                            account</a>
                    </div>
                </div>
                OpenDnD is a WebApplication developed with passion by Fermitech Softworks.
            </div>
        )
    }
}

class Dashboard extends React.Component {
    constructor(props) {
        super(props);
        this.state = {campaigns: [{title: null, owner: {uid: null, username: null}}]};
    }

    componentDidMount() {
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
                    this.setState({campaigns:result.campaigns})
                }
            });
    }

    render() {
        let ciao = [];
        for (let i = 0; i < 10; i++) {
            ciao.push(i);
        }
        return (
            <div>
                {ciao}
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