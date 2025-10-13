# init-rag-structure.ps1
$services = @("ingestion-service", "vector-store-service", "llm-service", "rag-orchestrator")
$commonDirs = @("common/utils")
$rootFiles = @("README.md", ".gitignore", "docker-compose.yml", ".env.example")

# Create root files
foreach ($file in $rootFiles) {
    if (-not (Test-Path $file)) {
        New-Item $file -ItemType File | Out-Null
    }
}

# Create common dirs
foreach ($dir in $commonDirs) {
    New-Item -ItemType Directory -Path $dir -Force | Out-Null
    New-Item -Path "$dir/__init__.py" -ItemType File -Force | Out-Null
}

# Create service directories
foreach ($service in $services) {
    $appPath = "$service/app"
    New-Item -ItemType Directory -Path $appPath -Force | Out-Null
    New-Item -Path "$appPath/__init__.py" -ItemType File -Force | Out-Null
    New-Item -Path "$appPath/main.py" -ItemType File -Force | Out-Null
    New-Item -Path "$service/pyproject.toml" -ItemType File -Force | Out-Null
    New-Item -Path "$service/Dockerfile" -ItemType File -Force | Out-Null
    New-Item -Path "$service/.gitignore" -ItemType File -Force | Out-Null
    New-Item -Path "$service/README.md" -ItemType File -Force | Out-Null
}
Write-Host "✅ Project structure created successfully."
