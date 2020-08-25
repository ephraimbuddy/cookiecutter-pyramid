<%inherit file="{{cookiecutter.app_name}}:templates/layout.mako"/>
<div class="content">
    <h1> Registeration </h1>
            <form action="${request.route_url('registration')}" method="post" id="register">
            ${msg}

             <input type="hidden" name="csrf_token" value="${get_csrf_token()}">

            <div class="form-group">
                <label for="email">Email</label>
                ${form.email(class_='form-control', id='email')}
                %for error in form.email.errors:
                    <div class="error">${error}</div>
                %endfor
            </div>

            <div class="form-group">
                <label for="username">Username</label>
                ${form.username(class_='form-control', id="username")}
                %for error in form.username.errors:
                    <div class="error">${error}</div>
                %endfor
            </div>

            <div class="form-group">
                <label for="password">Password</label>
                ${form.password(class_='form-control',id='password')}
                %for error in form.password.errors:
                    <div class="error">${error}</div>
                %endfor
            </div>
                <div class="form-group">
            <button type="submit" id="registerBtn" class="btn btn-success btn-lg">Register</button>
                    </div>

        </form>
 </div>