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

    character_builder = () => {
        console.log("Character_builder")
        this.setState({
            user: {
                uid: this.state.user.uid,
                token: this.state.user.token,
                username: this.state.user.username
            }, page: 'char_builder'
        })
    };

    dashboard = () => {
        console.log("Dashboard")
        this.setState({
            user: {
                uid: this.state.user.uid,
                token: this.state.user.token,
                username: this.state.user.username
            }, page: 'dashboard'
        })
    }


    render() {
        if (this.state.page === 'login') {
            return <Login loginFunc={this.validate} signupFunc={this.signup}></Login>
        } else if (this.state.page === 'dashboard') {
            return <Dashboard token={this.state.user.token} uid={this.state.user.uid}
                              charBuildFunc={this.character_builder}></Dashboard>
        } else if (this.state.page === 'char_builder') {
            return <CharBuilder token={this.state.user.token} uid={this.state.user.uid}
                                dashboardFunc={this.dashboard}></CharBuilder>
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
        this.state = {
            campaigns: [{title: null, owner: {uid: null, username: null}, cid: null}],
            characters: [{cid: null, name: null, race: null, level: null}]
        };
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

    gatherCharactersData() {
        let data = new FormData();
        data.append("token", this.props.token);
        data.append("uid", this.props.uid);
        fetch("/api/get_characters", {
            "method": "POST",
            "body": data
        })
            .then(res => res.json())
            .then((result) => {
                if (result.result === "failure") {
                    console.log(result.desc)
                } else if (result.result === "success") {
                    this.setState({characters: result.characters})
                }
            });
    }

    componentDidMount() {
        this.gatherCampaignData()
        this.gatherCharactersData()
    }

    render() {
        let campaigns = this.state.campaigns.map((item) => {
            return (
                <div key={"camp".concat(item.cid)}>{item.title}</div>
            )
        })
        let characters = this.state.characters.map((item) => {
            return (
                <div key={"char".concat(item.cid)}>{item.name} {item.race} {item.level}</div>
            )
        })
        return (
            <div className="dashboard-container">
                <br></br>
                <div className="container">
                    <div className="jumbotron trasparent">
                        <h1 className="display-3">Welcome to your dashboard,</h1>
                        <p></p>
                    </div>
                    <div className="btn-group">
                        <button type="button" className="btn btn-info">Actions</button>
                        <button type="button" className="btn btn-danger dropdown-toggle dropdown-toggle-split"
                                data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                            <span className="sr-only">Toggle Dropdown</span>
                        </button>
                        <div className="dropdown-menu">
                            <button className="dropdown-item" type="button" onClick={this.props.charBuildFunc}>Add a
                                character
                            </button>
                            <a className="dropdown-item" href="#">Add a skill</a>
                            <a className="dropdown-item" href="#">Add a class</a>
                            <div className="dropdown-divider"></div>
                            <a className="dropdown-item" href="#">Add a campaign</a>
                            <div className="dropdown-divider"></div>
                            <a className="dropdown-item" href="#">Account settings</a>
                        </div>
                    </div>
                    <div className="container">
                        <div className="row">
                            <div className="col-md-6 white">
                                {campaigns}
                            </div>
                            <div className="col-md-6 white">
                                {characters}
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        )
    }
}

class CharBuilder extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            skills: [{sid: null, name: null, attribute: null, desc: null}],
            counter: 0
        };
    }

    gatherSkillData() {
        let data = new FormData();
        data.append("token", this.props.token);
        data.append("uid", this.props.uid);
        fetch("/api/get_skills", {
            "method": "POST",
            "body": data
        })
            .then(res => res.json())
            .then((result) => {
                if (result.result === "failure") {
                    console.log(result.desc)
                } else if (result.result === "success") {
                    this.setState({skills: result.skills})
                }
            });
    }

    componentDidMount() {
        this.gatherSkillData()
    }

    addskill = () => {
        let skillset = this.state.skills.map((item) => {
            return (
                <option value={item.sid}>{item.name}, {item.attribute}</option>
            )
        });
        let options = "<option value=\"volvo\">Full</option><option value=\"volvo\">Half</option><option value=\"volvo\">Expertise</option>";
        let skills = "<select id=\"skill" + this.state.counter + "\" class=\"form-control\">skillset</select>";
        let prof_level = "<select id=\"skill_level" + this.state.counter + "\" class=\"form-control\">"+options+"</select>"
        let final = "<div className=\"row\" id=\"skillrow"+this.state.counter+"\"><div className=\"col-md-8\">"+skills+"</div><div className=\"col-md-4\">"+prof_level+"</div></div>";
        $("#skill").append(final);
        this.setState({counter: this.state.counter + 1});
        $("#remskill").removeClass("disabled");
    };

    removeskill = () => {
        if (this.state.counter > 0) {
            $("#skillrow"+(this.state.counter - 1)).remove();
            this.setState({counter: this.state.counter - 1});
            if (this.state.counter == 0) {
                $("remskill").addClass("disabled");
            }
        }
    };

    render() {

        return (
            <div className="dashboard-container">
                <div className="container">
                    <br></br>
                    <div className="jumbotron trasparent">
                        <form>
                            <div className="row">
                                <div className="col-md-4">
                                    <label htmlFor="name">Character name</label>
                                    <input type="text" className="form-control" id="name"></input>
                                </div>
                                <div className="col-md-2">
                                    <label htmlFor="level">Level</label>
                                    <input type="number" className="form-control" id="level"></input>
                                </div>
                                <div className="col-md-2">
                                    <label htmlFor="align">Alignament</label>
                                    <input type="text" className="form-control" id="align"></input>
                                </div>
                                <div className="col-md-4">
                                    <label htmlFor="race">Race</label>
                                    <input type="text" className="form-control" id="race"></input>
                                </div>
                            </div>
                            <div className="row">
                                <div className="col-md-1">
                                    <label htmlFor="str">Strength</label>
                                    <input type="number" className="form-control" id="str"></input>
                                    <label htmlFor="dex">Dexterity</label>
                                    <input type="number" className="form-control" id="dex"></input>
                                    <label htmlFor="cos">Constitution</label>
                                    <input type="number" className="form-control" id="cos"></input>
                                    <label htmlFor="int">Intelligence</label>
                                    <input type="number" className="form-control" id="int"></input>
                                    <label htmlFor="wis">Wisdom</label>
                                    <input type="number" className="form-control" id="wis"></input>
                                    <label htmlFor="cha">Charisma</label>
                                    <input type="number" className="form-control" id="cha"></input>
                                </div>
                                <div className="col-md-5">
                                    <label htmlFor="skill"> List of skill proficiencies </label>
                                    <div id="skill">
                                        <p>
                                            <div id="addskill" className="btn btn-success" onClick={this.addskill}> Add
                                                a skill
                                            </div>
                                            <div id="remskill" className="btn btn-danger disabled"
                                                 onClick={this.removeskill}> Remove a skill
                                            </div>
                                        </p>
                                    </div>
                                </div>
                            </div>
                        </form>
                    </div>
                </div>
            </div>
        );
    }

}

ReactDOM.render(
    <div id="react-app">
        <OpenDnD></OpenDnD>
    </div>,
    document.getElementById('react-app')
);