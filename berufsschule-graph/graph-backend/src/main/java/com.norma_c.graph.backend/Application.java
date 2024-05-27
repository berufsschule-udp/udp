package com.norma_c.graph.backend;

import jakarta.servlet.http.HttpServletResponse;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.autoconfigure.security.servlet.SecurityAutoConfiguration;
import org.springframework.context.annotation.Bean;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;
import org.springframework.security.web.SecurityFilterChain;
import org.springframework.security.web.authentication.www.BasicAuthenticationFilter;

import static jakarta.servlet.http.HttpServletResponse.SC_FORBIDDEN;
import static org.springframework.boot.SpringApplication.run;

@SpringBootApplication(exclude = { SecurityAutoConfiguration.class })
@EnableWebSecurity
public class Application {
	public static void main(String[] args) {
		run(Application.class, args);
	}

	@Bean
	public SecurityFilterChain filterChain(
		HttpSecurity httpSecurity
	) throws Exception {
		return httpSecurity
			.addFilterBefore((request, response, chain) -> {
				if (request.getRemoteAddr().equals("127.0.0.1")) {
					chain.doFilter(request, response);
				} else {
					((HttpServletResponse) response).setStatus(SC_FORBIDDEN);
				}
			}, BasicAuthenticationFilter.class)
			.build();
	}
}