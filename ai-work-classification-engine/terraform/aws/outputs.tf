output "cluster_endpoint" {
  description = "EKS cluster endpoint"
  value       = aws_eks_cluster.ai-work-classification-engine_cluster.endpoint
}

output "cluster_name" {
  description = "EKS cluster name"
  value       = aws_eks_cluster.ai-work-classification-engine_cluster.name
}

output "database_endpoint" {
  description = "RDS database endpoint"
  value       = aws_db_instance.ai-work-classification-engine_db.endpoint
  sensitive   = true
}

output "redis_endpoint" {
  description = "Redis cluster endpoint"
  value       = aws_elasticache_cluster.ai-work-classification-engine_cache.cache_nodes[0].address
}
