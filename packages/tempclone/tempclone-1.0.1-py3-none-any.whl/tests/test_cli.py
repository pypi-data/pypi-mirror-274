import pytest
from click.testing import CliRunner
import requests_mock
import subprocess
from tempclone.cli import cli, get_config, save_config

@pytest.fixture
def runner():
    return CliRunner()

@pytest.fixture
def mock_config(monkeypatch):
    config = {
        'token': 'fake_token',
        'nickname': 'fake_user'
    }
    monkeypatch.setattr('tempclone.cli.get_config', lambda: config)
    return config

def test_configure(runner):
    result = runner.invoke(cli, ['configure'], input='fake_token\nfake_user\n')
    assert result.exit_code == 0
    assert "Configuration saved successfully." in result.output

def test_list_templates(runner, mock_config):
    with requests_mock.Mocker() as m:
        m.get('https://api.github.com/users/fake_user/repos?page=1&per_page=100', json=[
            {'name': 'template1', 'is_template': True},
            {'name': 'template2', 'is_template': True},
            {'name': 'not_a_template', 'is_template': False},
        ])
        m.get('https://api.github.com/users/fake_user/repos?page=2&per_page=100', json=[])
        result = runner.invoke(cli, ['list-templates'])
        print(result.output)  # Debug output
        assert result.exit_code == 0
        assert "template1" in result.output
        assert "template2" in result.output
        assert "not_a_template" not in result.output

def test_new_project(runner, mock_config, monkeypatch):
    with requests_mock.Mocker() as m:
        m.get('https://api.github.com/users/fake_user/repos?page=1&per_page=100', json=[
            {'name': 'template1', 'is_template': True},
        ])
        m.get('https://api.github.com/users/fake_user/repos?page=2&per_page=100', json=[])
        m.post('https://api.github.com/repos/fake_user/template1/generate', json={
            'clone_url': 'https://github.com/fake_user/new_project'
        }, status_code=201)
        m.get('https://api.github.com/repos/fake_user/new_project', json={
            'size': 1
        })

        def mock_subprocess_run(*args, **kwargs):
            print(f"Mocked subprocess.run called with: {args}")
            return subprocess.CompletedProcess(args, 0)
        
        monkeypatch.setattr(subprocess, 'run', mock_subprocess_run)
        
        result = runner.invoke(cli, ['new-project', 'new_project'], input='fake_user\n1\n')
        print(result.output)  # Debug output
        assert result.exit_code == 0
        assert "New repository created" in result.output
        assert "https://github.com/fake_user/new_project" in result.output
        assert "Project new_project successfully set up!" in result.output
