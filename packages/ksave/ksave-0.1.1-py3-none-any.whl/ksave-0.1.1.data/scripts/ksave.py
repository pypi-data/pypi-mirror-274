#!python

## Command Imports
import ksave

import argparse
import sys

## Command Imports
from ksave.src.commands.pods import Pods
from ksave.src.commands.deployments import Deployments
from ksave.src.commands.statefulsets import StatefulSets
from ksave.src.commands.daemonsets import DaemonSets
from ksave.src.commands.jobs import Jobs
from ksave.src.commands.cronjobs import CronJobs
from ksave.src.commands.secrets import Secrets
from ksave.src.commands.configmaps import ConfigMaps
from ksave.src.commands.ingress import Ingress
from ksave.src.commands.services import Services
from ksave.src.commands.storageclass import StorageClass
from ksave.src.commands.persistentvolumes import PersistentVolume
from ksave.src.commands.persistentvolumeclaims import PersistentVolumeClaim
from ksave.src.commands.serviceaccounts import ServiceAccount
from ksave.src.commands.roles import Role
from ksave.src.commands.rolebindings import RoleBinding
from ksave.src.commands.clusterroles import ClusterRole
from ksave.src.commands.clusterrolebindings import ClusterRoleBinding

class KSave(object):

    def __init__(self):
        # create the top-level parser
        parser = argparse.ArgumentParser(prog='ksave')
        # create sub-parser
        sub_parser = parser.add_subparsers(help='sub-command help',dest="subcommand")
        
        # create sub-commands
        subcommands=dict()
        subcommands["podsCommand"] = Pods(sub_parser)
        subcommands["deploymentsCommand"] = Deployments(sub_parser)
        subcommands["daemonsetsCommand"] = DaemonSets(sub_parser)
        subcommands["statefulsetsCommand"] = StatefulSets(sub_parser)
        subcommands["cronjobsCommand"] = CronJobs(sub_parser)
        subcommands["jobsCommand"] = Jobs(sub_parser)
        subcommands["secretsCommand"] = Secrets(sub_parser)
        subcommands["configmapsCommand"] = ConfigMaps(sub_parser)
        subcommands["ingressCommand"] = Ingress(sub_parser)
        subcommands["servicesCommand"] = Services(sub_parser)
        subcommands["storageclassCommand"] = StorageClass(sub_parser)
        subcommands["persistentvolumesCommand"] = PersistentVolume(sub_parser)
        subcommands["persistentvolumeclaimsCommand"] = PersistentVolumeClaim(sub_parser)
        subcommands["serviceaccountCommand"] = ServiceAccount(sub_parser)
        subcommands["rolesCommand"] = Role(sub_parser)
        subcommands["rolebindingsCommand"] = RoleBinding(sub_parser)
        subcommands["clusterrolesCommand"] = ClusterRole(sub_parser)
        subcommands["clusterrolebindingsCommand"] = ClusterRoleBinding(sub_parser)

        ## Finally parse all arguments
        args = parser.parse_args()

        ## Run related object functions
        className = str(args.subcommand) + "Command"
        getattr(subcommands[className], "run")(args)

        return


if __name__ == "__main__":
    KSave()