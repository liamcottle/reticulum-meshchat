#!/bin/bash

PGreen='\033[0;32m'
PRed='\033[0;31m'
PNC='\033[0m'

print_info() {
  echo -e "${PGreen}${1}${PNC}"
}

print_warn() {
  echo -e "${PRed}${1}${PNC}"
}

check_proceed() {
	if [[ ${1} == "n" ]] || [[ ${1} == "N" ]]; then 
		return 1
	elif [[ ${1} == "y" ]] || [[ ${1} == "Y" ]]; then
		return 0
	elif [[ ${1} == "" ]] && [[ ${2} == "N" ]]; then
		return 1
	elif [[ ${1} == "" ]] && [[ ${2} == "Y" ]]; then
		return 0
	else
		print_warn "Invalid selection, Aborting..."
		exit 1
	fi
}

check_group_memberships() {
	if egrep -q "^sudo.*$(whoami)" /etc/group; then 
		print_info "User in sudo group."
		UserInSudo=1
	else
		print_warn "User not in sudo group.\nThis script requires sudo cause I'm lazy to write it better, Aborting..."
		UserInSudo=0
		exit 1
	fi
	if egrep -q "^dialout.*$(whoami)" /etc/group; then 
		print_info "User in dialout group."
		UserInDialout=1
	else
		print_warn "User not in dialout group.\nSome script functions will not run."
		UserInDialout=0
	fi
	if egrep -q "^docker.*$(whoami)" /etc/group; then
		print_info "User in docker group."
		UserInDocker=1
	else
		print_warn "User not in docker group.\nJust a heads up, not a blocker."
		UserInDocker=0
	fi
}

check_installed_programs() {
	if [[ -f $(which rnodeconf) ]]; then
		print_info "rnodeconf available on host."
		RnodeconfAvail=1
	else
		print_warn "rnodeconf not available on host.\nSome script functions will not run."
		RnodeconfAvail=0
	fi
}

check_existing_meshchat_ctr() {
	if sudo docker ps | awk '{print $NF}' | grep -q "meshchat"; then
		MeshChatCtrRunning=1
	fi
	
	MeshChatCtrExists=0
	if sudo docker ps -a | awk '{print $NF}' | grep -q "meshchat"; then
		MeshChatCtrExists=1
	fi

	if [[ ${MeshChatCtrRunning} == 1 ]]; then
		read -p "Meshchat container is running, stop? [y/N] " StopMeshChatCtr
		if check_proceed ${StopMeshChatCtr} "N"; then
			print_info "Running: sudo docker stop meshchat"
			sudo docker stop meshchat
		else
			print_warn "Kept running container, Exiting..."
			exit 0
		fi;
	fi;

	if [[ ${MeshChatCtrExists} == 1 ]]; then
		read -p "Meshchat container exists, remove? [y/N] " RmMeshChatCtr
		if check_proceed ${RmMeshChatCtr} "N"; then
			print_info "Running: sudo docker rm -f meshchat"
			sudo docker rm -f meshchat
			MeshChatCtrExists=0
		else
			print_warn "Kept existing container, Exiting..."
			exit 0
		fi;
	fi;
}

check_existing_confs_and_backup() {
	if sudo [ -d /var/lib/docker/volumes/meshchat_config/_data ]; then
		print_info "Found pre-existing volume at: /var/lib/docker/volumes/meshchat_config/_data";
		read -p "Backup now? [Y/n]" BackupConfigs
		if check_proceed ${BackupConfigs} "Y"; then
			DateTime=$(date '+%Y-%m-%dT%H-%M-%S')
			mkdir ${DateTime}_meshchat_bak
			sudo cp -r /var/lib/docker/volumes/meshchat_config/_data/.{reticulum,meshchat} ${DateTime}_meshchat_bak/
			sudo chown -R nobody:nogroup ${DateTime}_meshchat_bak
			tar czf ${DateTime}_meshchat_bak.tar.gz ${DateTime}_meshchat_bak
			sudo rm -rf ${DateTime}_meshchat_bak
		fi
	fi
}

check_existing_meshchat_volume() {
	if sudo docker volume ls | grep -q "meshchat_config"; then
		MeshChatVolExists=1
		read -p "Meshchat volume exists, re-create: [y/N] " RecreateMeshChatVol
	else
		MeshChatVolExists=0
	fi
	
	if [[ ${MeshChatVolExists} == 1 ]] && check_proceed ${RecreateMeshChatVol} "N"; then
		RecreateMeshChatVol=1
	fi

	if [[ ${MeshChatVolExists} == 0 ]]; then
		print_info "Running: sudo docker volume create meshchat_config"
		sudo docker volume create meshchat_config
		MeshChatVolNew=1
	elif [[ ${RecreateMeshChatVol} == 1 ]]; then
		print_info "Running: sudo docker volume rm -f meshchat_config"
		sudo docker volume rm -f meshchat_config
		print_info "Running: sudo docker volume create meshchat_config"
		sudo docker volume create meshchat_config
		MeshChatVolNew=1
	else
		MeshChatVolNew=0
	fi
}

get_rnode_ttys() {
	TtyDevNum=0
	if [[ ${UserInDialout} == 1 ]] && [[ ${RnodeconfAvail} == 1 ]]; then
		print_info "Enumerating TTYs, please be patient..."
	else
		print_warn "Since user is not in dialout and/or rnodeconf is not installed cannot check TTYs for RNode firmware.\nTake care to select the appropriate TTY(s)."
	fi
	for TtyDev in $(ls /dev/tty{ACM,USB}* 2> /dev/null); do
		TtyDevs[${TtyDevNum}]=${TtyDev}
		echo "${TtyDevNum} : ${TtyDev}"
		TtyDevNum=$((${TtyDevNum}+1))
		if [[ ${UserInDialout} == 1 ]] && [[ ${RnodeconfAvail} == 1 ]]; then
			rnodeconf -i ${TtyDev} 2>&1 | egrep -o "(Product|Device signature|Firmware version|Hardware revision|Serial number|Modem chip|Frequency range|Max TX power|Manufactured|Device mode).*"
			echo ""
		fi
	done

	if [[ ${#TtyDevs[@]} > 0 ]]; then
		read -p "TTY dev(s) identified, select any R-Node TTY(s), space delimited: " RnodeTtyDevIndicies
		if echo ${RnodeTtyDevIndicies} | egrep -q "^[0-9]$|^([0-9] )+[0-9]$"; then
			for RnodeTtyDevIndex in ${RnodeTtyDevIndicies}; do
				if [[ ${TtyDevs[${RnodeTtyDevIndex}]} != "" ]]; then
					RnodeTtysSelected=1
					DockerTtyDevsString="${DockerTtyDevsString} --device=${TtyDevs[${RnodeTtyDevIndex}]}"
				fi
			done
		elif echo ${RnodeTtyDevIndicies} | egrep -q "^$"; then
			print_info "No TTY devices selected, continuing..."
		else
			print_warn "Invalid TTY device index identified, exiting..."
			exit 1
		fi
	fi
}

create_meshchat_ctr() {
	if [[ ${MeshChatCtrExists} == 0 ]]; then
		if [[ ${RnodeTtysSelected} == 1 ]]; then
			print_info "Running: sudo docker run --detach --pull always --name meshchat --restart unless-stopped --publish 8000:8000 --volume meshchat_config:/config ${DockerTtyDevsString} ghcr.io/liamcottle/reticulum-meshchat:latest"
			bash -c "sudo docker run --detach --pull always --name meshchat --restart unless-stopped --publish 8000:8000 --volume meshchat_config:/config ${DockerTtyDevsString} ghcr.io/liamcottle/reticulum-meshchat:latest"
		else
			print_info "Running: sudo docker run --detach --pull always --name meshchat --restart unless-stopped --publish 8000:8000 --volume meshchat_config:/config ghcr.io/liamcottle/reticulum-meshchat:latest"
			bash -c "sudo docker run --detach --pull always --name meshchat --restart unless-stopped --publish 8000:8000 --volume meshchat_config:/config ghcr.io/liamcottle/reticulum-meshchat:latest"
		fi
	fi
}

restore_config_or_backup() {
	BackupNum=0
	for Backup in $(ls | egrep "[0-9]{4}-[0-1][0-9].*meshchat_bak.tar.gz" 2> /dev/null); do
		Backups[${BackupNum}]=${Backup}
		echo "${BackupNum} : ${Backup}"
		BackupNum=$((${BackupNum}+1))
	done
	if [[ ${#Backups[@]} > 0 ]]; then
		print_info "Backups identified. If desired one may be restored."
		print_warn "Note that backup restore is a full restore, any messages or changes since the backup had been taken may be lost if not on propogation net."
		read -p "If desired select a backup to restore: " BackupToRestore 
	fi
	if [[ ${BackupToRestore} == "" ]]; then
		print_info "No backup selected to be restored."
	elif [[ ${BackupToRestore} != "" ]] && [[ ${Backups[${BackupToRestore}]} != "" ]]; then
		UntarDir=$(echo ${Backups[${BackupToRestore}]} | sed 's/.tar.gz//g')
		print_info "Running: tar xf ${Backups[${BackupToRestore}]}"
		tar xf ${Backups[${BackupToRestore}]}
		print_info "Running: sudo docker stop meshchat"
		sudo docker stop meshchat
		print_info "Running: sudo rm -rf /var/lib/docker/volumes/meshchat_config/_data/.{reticulum,meshchat}"
		sudo rm -rf /var/lib/docker/volumes/meshchat_config/_data/.{reticulum,meshchat}
		print_info "Running: sudo cp -R ${UntarDir}/.{reticulum,meshchat} /var/lib/docker/volumes/meshchat_config/_data/"
		sudo cp -R ${UntarDir}/.{reticulum,meshchat} /var/lib/docker/volumes/meshchat_config/_data/
		print_info "Running: sudo rm -rf ${UntarDir}"
		sudo rm -rf ${UntarDir}
		print_info "Running: sudo docker start meshchat"
		sudo docker start meshchat
	else
		print_warn "Invalid backup index selected, Aborting..."
	fi
	if [[ -f config ]]; then
		read -p "Config found at $(pwd)/config, copy into volume? [y/N] " CopyInExistingConfig
	fi
	if check_proceed ${CopyInExistingConfig} "N"; then
		sleep 1
		print_info "Running: sudo docker cp ./config meshchat:/config/.reticulum/config"
		sudo docker cp ./config meshchat:/config/.reticulum/config
		print_info "Running: sudo docker restart meshchat"
		sudo docker restart meshchat
		sleep 2
	fi
	print_info "Unless you edited your configs meshchat should be reachable below in a few moments.\nhttp://localhost:8000"
	
}

check_group_memberships
check_installed_programs
check_existing_meshchat_ctr
check_existing_confs_and_backup
check_existing_meshchat_volume
get_rnode_ttys
create_meshchat_ctr
restore_config_or_backup
