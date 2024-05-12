from subprocess import check_output, CalledProcessError

responses = []

for IP in (
    "142.251.40.164",
    "104.21.54.180",
    "5.255.255.242"
):
    try:
        response = check_output(
            f'ping -n 1 -w 500 {IP}',
            shell=True,
            encoding=str(
                check_output('chcp', shell=True)
            ).split(':')[-1][1:].split('\\')[0]
        )
        print(response)
        responses.append("(0% " in response)
    except CalledProcessError as CPE:
        print(CPE.output)
        responses.append(False)

print(any(responses))
