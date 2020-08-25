<%inherit file="{{cookiecutter.app_name}}:templates/layout.mako"/>

<div class="content">
    <div class="form-wrap">
         <form  method="post" class="form-horizontal" id="signIn">
            <input type="hidden" name="csrf_token" value="${get_csrf_token()}">
            ${message}
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
            </div>

            <div class="col-md-12">
                <div class="form-group">
            <button type="submit" class="btn btn-primary">Log In</button>
                    </div>
            </div>
        </form>
    </div>
</div>