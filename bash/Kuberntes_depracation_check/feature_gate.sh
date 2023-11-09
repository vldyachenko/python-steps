#!/bin/bash
list=./pod_securitypolicies.txt
if [ -f "$list" ]; then
echo "Stack list file is present, removing"
rm pod_security.txt
else
echo "Stack list file is not present, going on"

fi

cluster_name=$(kubectl config current-context)
echo "Cluster name: $cluster_name" >> pod_securitypolicies.txt

namespace=$( kubectl get podsecuritypolicy --all-namespaces=true | awk -F ' ' '{print $1}' | grep -wv NAMESPACE | uniq)
for i in $namespace
do 
echo "Namespace: $i" >> pod_securitypolicies.txt
hpa_list=$(kubectl get podsecuritypolicy --all-namespaces=true -n $i | grep -wv NAME | awk -F ' ' '{print $1}')
for x in $hpa_list 
do
echo "HPA name  is $x " >> pod_securitypolicies.txt
kubectl get pod $x -n $i -o yaml  | grep feature>> pod_securitypolicies.txt
done
done

echo "PodSecurityPolicies that will be deprecated: $(kubectl get podsecuritypolicy --all-namespaces=true) " >> pod_securitypolicies.txt
