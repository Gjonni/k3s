{{/*
Expand the name of the chart.
*/}}
{{- define "fclinica-2023.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Create a default fully qualified app name.
We truncate at 63 chars because some Kubernetes name fields are limited to this (by the DNS naming spec).
If release name contains chart name it will be used as a full name.
*/}}
{{- define "fclinica-2023.fullname" -}}
{{- if .Values.fclinica.fullnameOverride }}
{{- .Values.fclinica.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- $name := default .Chart.Name .Values.nameOverride }}
{{- if contains $name .Release.Name }}
{{- .Release.Name | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}
{{- end }}

{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "fclinica-2023.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "fclinica-2023.labels" -}}
helm.sh/chart: {{ include "fclinica-2023.chart" . }}
{{ include "fclinica-2023.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "fclinica-2023.selectorLabels" -}}
app.kubernetes.io/name: {{ include "fclinica-2023.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}

{{/*
Create the name of the service account to use
*/}}
{{- define "fclinica-2023.serviceAccountName" -}}
{{- if .Values.fclinica.serviceAccount.create }}
{{- default (include "fclinica-2023.fullname" .) .Values.fclinica.serviceAccount.name }}
{{- else }}
{{- default "default" .Values.fclinica.serviceAccount.name }}
{{- end }}
{{- end }}
