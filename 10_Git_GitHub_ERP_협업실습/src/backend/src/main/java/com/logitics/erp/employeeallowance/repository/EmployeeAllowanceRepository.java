package com.logitics.erp.employeeallowance.repository;

import com.logitics.erp.employeeallowance.entity.EmployeeAllowance;
import org.springframework.data.jpa.repository.JpaRepository;

public interface EmployeeAllowanceRepository extends JpaRepository<EmployeeAllowance, Long> {
}
