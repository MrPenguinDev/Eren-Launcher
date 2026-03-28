from eren_launcher.launch import build_bedrock_launch_command


def test_build_bedrock_launch_command_no_auth_required() -> None:
    cmd = build_bedrock_launch_command("mobile", ["pack_a", "pack_b"])
    assert cmd == ["bedrock", "--profile", "mobile", "--pack", "pack_a", "--pack", "pack_b"]
