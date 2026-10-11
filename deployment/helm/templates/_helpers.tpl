{{- define "EphapticOS.name" -}}
{{- .Chart.Name | trunc 63 | trimSuffix "-" }}
{{- end }}

{{- define "EphapticOS.fullname" -}}
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

{{- define "EphapticOS.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{- define "EphapticOS.labels" -}}
helm.sh/chart: {{ include "EphapticOS.chart" . }}
{{ include "EphapticOS.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{- define "EphapticOS.selectorLabels" -}}
app.kubernetes.io/name: {{ include "EphapticOS.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}

{{- define "EphapticOS.serviceAccountName" -}}
{{- if .Values.serviceAccount.create }}
{{- default (include "EphapticOS.fullname" .) .Values.serviceAccount.name }}
{{- else }}
{{- default "default" .Values.serviceAccount.name }}
{{- end }}
{{- end }}

{{- define "EphapticOS.postgres.fullname" -}}
{{- printf "%s-postgres" (include "EphapticOS.fullname" .) }}
{{- end }}
