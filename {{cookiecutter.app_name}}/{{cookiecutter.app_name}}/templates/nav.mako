<nav class="navbar navbar-expand-md navbar-dark fixed-top bg-dark">
  <a class="navbar-brand" href="${request.route_url('home')}">{{cookiecutter.project_name}}</a>
  <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarsExampleDefault" aria-controls="navbarsExampleDefault" aria-expanded="false" aria-label="Toggle navigation">
    <span class="navbar-toggler-icon"></span>
  </button>

  <div class="collapse navbar-collapse" id="navbarsExampleDefault">
    <ul class="navbar-nav mr-auto">
      <li class="nav-item active">
        <a class="navbar-brand" href="${request.route_url('home')}">
        Home
        <span class="sr-only">(current)</span></a>
      </li>
      </ul>

    <ul class="navbar-nav navbar-right">
    %if request.user:
      <li class="nav-item">
        <a class="nav-link" href="${request.route_url('logout')}">
          Logout
        </a>
      </li>
     %else:
        <li class="nav-item">
        <a class="nav-link" href="${request.route_url('login')}">Log in</a>
      </li>
      <li class="nav-item">
        <a class="nav-link" href="${request.route_url('registration')}">Create account</a>
      </li>
    %endif
    </ul>
  </div>
</nav>
