<%inherit file="{{cookiecutter.app_name}}:templates/layout.mako"/>

    <div class="login-wrap">
        <h1> Login </h1>
         <form  method="post" class="form-horizontal" id="signIn">
            <input type="hidden" name="csrf_token" value="${get_csrf_token()}">
            <div class="form-group">
                <label for="username">Username</label>
                ${form.username(class_='form-control')}
                %for error in form.username.errors:
                    <div class="text-danger">${error}</div>
                %endfor
            </div>

            <div class="form-group">
                <label for="password">Password</label>
                ${form.password(class_='form-control')}
                %for error in form.password.errors:
                    <div class="text-danger">${error}</div>
                %endfor
            </div>

                <div class="form-group">
            <button type="submit" class="btn btn-primary">Log In</button>
                    </div>

         </form>
    </div>
