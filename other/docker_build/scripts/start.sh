start_nginx() {
    echo "Starting Nginx service..."
    service nginx start
}

# Execute script if exists
execute_script() {
    local script_path=$1
    local script_msg=$2
    if [[ -f ${script_path} ]]; then
        echo "${script_msg}"
        bash ${script_path}
    fi
}

export_env_vars() {
    echo "Exporting environment variables..."
    printenv | grep -E '^RUNPOD_|^PATH=|^_=' | awk -F = '{ print "export " $1 "=\"" $2 "\"" }' >> /etc/rp_environment
    echo 'source /etc/rp_environment' >> ~/.bashrc
}

# Start jupyter lab
start_jupyter() {
    if [[ $JUPYTER_PASSWORD ]]; then
        echo "Starting Jupyter Lab..."
        mkdir -p /workspace && \
        cd / && \
        nohup jupyter lab --allow-root --no-browser --port=8888 --ip=* --FileContentsManager.delete_to_trash=False --ServerApp.terminado_settings='{"shell_command":["/bin/bash"]}' --ServerApp.token=$JUPYTER_PASSWORD --ServerApp.allow_origin=* --ServerApp.preferred_dir=/workspace &> /jupyter.log &
        echo "Jupyter Lab started"
    fi
}

start_comfy_ui() {
    echo "Starting ComfyUI..."
    COMFY_UI_DIR="/workspace/comfy_ui"
    cd $COMFY_UI_DIR
    nohup python main.py --listen --port 8188 &> /comfy_ui_nohup.log &
    echo "ComfyUI Lab started"
}



start_nginx

execute_script "/pre_start.sh" "Running pre-start script..."

echo "Pod Started"
echo "+++ confi at $COMFY"

start_comfy_ui
start_jupyter

export_env_vars

execute_script "/post_start.sh" "Running post-start script..."

echo "Start script(s) finished, pod is ready to use."
sleep 10s
jupyter server list

sleep infinity