{{/*
Expand the name of the chart.
*/}}
{{- define "home-task.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}


{{/*
Expand the name of the chart.
*/}}
{{- define "home-task.fullname" -}}
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
{{- define "home-task.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}



{{/*
Expand the namespace of the chart.
*/}}
{{- define "home-task.namespace" -}}
{{- if .Values.namespace }}
{{- .Values.namespace | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- default .Release.Namespace }}
{{- end }}
{{- end }}

{{/*
Expand the port of the chart.
*/}}
{{- define "home-task.port" -}}
{{- .Values.service.port | trunc 63 | trimSuffix "-" }}
{{- end }}


{{/*
Common labels
*/}}
{{- define "home-task.labels" -}}
app: {{ include "home-task.name" . }}
chart: {{ include "home-task.chart" . }}
release: {{ .Release.Name }}
heritage: {{ .Release.Service }}
{{- end -}}

{{/*
Selector labels
*/}}
{{- define "home-task.selectorLabels" -}}
app: {{ include "home-task.name" . }}
release: {{ .Release.Name }}
{{- end -}}

{{/*
Create the name of the service account to use
*/}}
{{- define "home-task.serviceAccountName" -}}
{{- if .Values.serviceAccount.create }}
{{- default (include "home-task.fullname" .) .Values.serviceAccount.name }}
{{- else }}
{{- default "default" .Values.serviceAccount.name }}
{{- end }}
{{- end }}

{{/*
Create the name of the service to use
*/}}
{{- define "home-task.serviceName" -}}
{{- include "home-task.fullname" . }}
{{- end }}

{{/*
Create the name of the service to use
*/}}
{{- define "home-task.PodDisruptionBudgetName" -}}
{{- include "home-task.fullname" . }}
{{- end }}