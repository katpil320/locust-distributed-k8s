{{/*
Expand the name of the chart.
*/}}
{{- define "locust-distributed.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Create a default fully qualified app name.
We truncate at 63 chars because some Kubernetes name fields are limited to this (by the DNS naming spec).
If release name contains chart name it will be used as a full name.
*/}}
{{- define "locust-distributed.fullname" -}}
{{- if .Values.fullnameOverride }}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" }}
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
{{- define "locust-distributed.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "locust-distributed.labels" -}}
helm.sh/chart: {{ include "locust-distributed.chart" . }}
{{ include "locust-distributed.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "locust-distributed.selectorLabels" -}}
app.kubernetes.io/name: {{ include "locust-distributed.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}

{{/*
Create the name of the service account to use
*/}}
{{- define "locust-distributed.serviceAccountName" -}}
{{- if .Values.serviceAccount.create }}
{{- default (include "locust-distributed.fullname" .) .Values.serviceAccount.name }}
{{- else }}
{{- default "default" .Values.serviceAccount.name }}
{{- end }}
{{- end }}

{{/*
Locust master labels
*/}}
{{- define "locust-distributed.masterLabels" -}}
{{ include "locust-distributed.labels" . }}
app.kubernetes.io/component: master
{{- end }}

{{/*
Locust master selector labels
*/}}
{{- define "locust-distributed.masterSelectorLabels" -}}
{{ include "locust-distributed.selectorLabels" . }}
app.kubernetes.io/component: master
{{- end }}

{{/*
Locust worker labels
*/}}
{{- define "locust-distributed.workerLabels" -}}
{{ include "locust-distributed.labels" . }}
app.kubernetes.io/component: worker
{{- end }}

{{/*
Locust worker selector labels
*/}}
{{- define "locust-distributed.workerSelectorLabels" -}}
{{ include "locust-distributed.selectorLabels" . }}
app.kubernetes.io/component: worker
{{- end }}

{{/*
File browser labels
*/}}
{{- define "locust-distributed.filebrowserLabels" -}}
{{ include "locust-distributed.labels" . }}
app.kubernetes.io/component: filebrowser
{{- end }}

{{/*
File browser selector labels
*/}}
{{- define "locust-distributed.filebrowserSelectorLabels" -}}
{{ include "locust-distributed.selectorLabels" . }}
app.kubernetes.io/component: filebrowser
{{- end }}
